import datetime
import random


from celery import shared_task
from rest_framework.request import Request
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from myschool import settings
from services.mixins import UserIsAuthenticated, UserAuthAccess
from .forms import RegistrationForm, LoginForm
from .models import Profile, PreRegistrationData


def generate_code() -> int:
    random.seed()
    code = random.randint(100000, 999999)
    return code


def generate_and_send(recipient: str, request: Request):
    code: int = generate_code()
    request.session['code'] = code
    send_mail(
        'Подтвердите свой электронный адрес',
        f'Введите следующий код, чтобы подтвердить e-mail и завершить регистрацию:\n'
        f'{code}',
        settings.EMAIL_HOST_USER,
        [recipient],
        fail_silently=False,
    )


def send_activate_email_message(request: Request, recipient: str) -> dict:
    if not request.session.get('send_count'):
        request.session['send_count'] = 1
    send_count = request.session['send_count']
    print(send_count)
    if send_count <= 2:
        request.session['send_count'] += 1
        request.session['sending_time'] = datetime.datetime.strftime(datetime.datetime.now(),
                                                                     '%Y-%m-%d %H:%M:%S')
        generate_and_send(recipient=recipient, request=request)
        timer_run = False if send_count != 2 else True

        return {
            'access': True,
            'timer_run': timer_run,
            'timer': 300
        }
    else:
        now_time = datetime.datetime.now()
        send_time = datetime.datetime.strptime(request.session.get('sending_time'), '%Y-%m-%d %H:%M:%S')
        delta_time = now_time - send_time
        if delta_time.seconds > 300:
            request.session['sending_time'] = datetime.datetime.strftime(datetime.datetime.now(),
                                                                         '%Y-%m-%d %H:%M:%S')
            generate_and_send(recipient=recipient, request=request)
            return {
                'access': True,
                'timer_run': False,
            }
        else:
            return {
                'access': False,
                'timer_run': True,
                'timer': 300 - delta_time.seconds
            }


def get_timer(request: Request) -> dict:
    send_count = request.session.get('send_count')
    timer = 0
    if send_count:
        if send_count > 2:
            now_time = datetime.datetime.now()
            send_time = datetime.datetime.strptime(request.session.get('sending_time'), '%Y-%m-%d %H:%M:%S')
            delta_time = now_time - send_time
            if delta_time.seconds < 300:
                run_timer = True
                timer = 300 - delta_time.seconds
            else:
                run_timer = False
        else:
            run_timer = False
    else:
        run_timer = False

    return {
        'timer_run': run_timer,
        'timer': timer
    }


def formate_time(time: int) -> str:
    left_part = '00' if time // 60 == 0 else f'0{time // 60}'
    right_part = f'0{time % 60}' if time % 60 < 10 else f'{time % 60}'
    return f'{left_part}:{right_part}'


class SendActivationCode(APIView):

    def get(self, request: Request) -> Response:
        email = request.session.get('email')
        response = send_activate_email_message(request=request, recipient=email)
        return Response({
            'access': response['access'],
            'timer_run': response['timer_run'],
            'timer': response.get('timer')
        })


class CheckUserEmail(APIView):
    def get(self, request: Request) -> Response:
        request.session['first_step'] = False
        timer = 0
        timer_run = False
        send_count = request.session['send_count']
        if send_count > 2:
            now_time = datetime.datetime.now()
            send_time = datetime.datetime.strptime(request.session.get('sending_time'), '%Y-%m-%d %H:%M:%S')
            delta_time = now_time - send_time
            if delta_time.seconds < 300:
                timer_run = True
                timer = 300 - delta_time.seconds
            else:
                timer_run = False
        return Response({
            'access': True,
            'timer_run': timer_run,
            'timer': timer
        })

    def post(self, request: Request) -> Response:
        email = request.data['email'].strip().lower()
        try:
            validate_email(email)
        except ValidationError as error:
            return Response({
                'access': False,
                'error': error
            })
        if User.objects.filter(email=email).exists():
            return Response({
                'access': False,
                'error': ['Пользователь с таким e-mail уже существует']
            })
        request.session['email'] = email
        response = send_activate_email_message(request=request, recipient=email)
        if response['access']:
            request.session['first_step'] = True
            return Response({
                'access': True,
            })
        return Response({
            'access': False,
            'timer_run': True,
            'time': response['timer'],
            'error': ['Превышен лимит отправок код. Пожалуйста, дождитесь окончания таймера.']
        })


class ConfirmUserEmail(APIView):

    def post(self, request: Request) -> Response:
        user_code: str = request.data.get('code')
        if not user_code.isdigit():
            return Response({
                'access': False,
                'error': 'Неверный формат кода.'
            })
        code = request.session.get('code')
        if int(user_code) == code:
            request.session['second_step'] = True
            return Response({'access': True})
        return Response({
            'access': False,
            'error': 'Введён неверный код. Попробуйте снова.'
        })


class RegisterView(UserIsAuthenticated, CreateView):
    template_name = 'users/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        #self.request.session.flush()
        first_step = self.request.session.get('first_step')
        second_step = self.request.session.get('second_step')
        third_step = self.request.session.get('third_step')

        current_timer = get_timer(self.request)

        context = super(RegisterView, self).get_context_data(**kwargs)
        context.update({
            'btn_title': 'зарегестрироваться',
            'first_step': first_step,
            'second_step': second_step,
            'third_step': third_step,
            'email': self.request.session.get('email'),
            'timer_run': current_timer['timer_run'],
            'timer': formate_time(current_timer['timer'])
        })

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        email = self.request.session['email']
        user = self.object
        user.username = email
        user.email = email
        user.save()
        login(self.request, user)
        phone = form.cleaned_data.get('phone')
        if phone.startswith('8'):
            phone = phone.replace('8', '+7', 1)
        new_profile = Profile(
            user=user,
            second_name=form.cleaned_data.get('second_name'),
            phone=phone,
            birth_date=form.cleaned_data.get('birth_date'),
            email_confirmed=False
        )
        new_profile.save()
        self.request.session.__delitem__('email')
        self.request.session.__delitem__('code')
        self.request.session.__delitem__('sending_time')
        self.request.session.__delitem__('first_step')
        self.request.session.__delitem__('second_step')
        return response

    def form_invalid(self, form):
        timer_run = False
        sending_time = self.request.session.get('sending_time')
        if sending_time:
            sending_time = datetime.datetime.strptime(sending_time, '%Y-%m-%d %H:%M:%S')
            now_time = datetime.datetime.now()
            delta_time = now_time - sending_time
            if delta_time.seconds < 300:
                timer_run = True
        return self.render_to_response(self.get_context_data(form=form, **{'errors': True, 'timer_run': timer_run}))


class LoginUserView(UserIsAuthenticated, LoginView):
    template_name = 'users/authorization.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('main')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('main')