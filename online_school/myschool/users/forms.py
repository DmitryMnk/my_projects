from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


def phone_validator(value: str):
    if not (value.startswith('+7') and len(value) == 12 or value.startswith('8') and len(value) == 11):
        raise ValidationError('Неверный формат номера телефона')
    else:
        phone = value.replace('8', '+7', 1) if value.startswith('8') else value

        if Profile.objects.filter(phone=phone).exists():
            raise ValidationError('Пользователь с таким номером телефона уже существует.')
        elif not phone[1:].isdigit():
            raise ValidationError('Телефон должен состоять только из цифр')


class RegistrationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=12,
        validators=[phone_validator],
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите номер телефона...'
        })
    )

    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-input',
                                    'placeholder': 'Введите пароль...',
                                    'autocomplete': 'new-password'
                                }),
                                max_length=30
                                )

    password2 = forms.CharField(label='Подтверждение пароля',
                                max_length=30,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-input',
                                    'placeholder': 'Подтвердите пароль...',
                                    'autocomplete': 'new-password'
    }))

    class Meta:
        model = User
        fields = 'password1', 'password2', 'first_name', 'last_name', 'phone'
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите Ваше Имя...'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите Вашу Фамилию...'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите пароль...'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Подтвердите пароль...'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует.')
        return email

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name').strip().title()
        return name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').strip().title()
        return last_name


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='e-mail', max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Введите email...',
        'name': 'email'
    }))
    password = forms.CharField(label='Пароль', max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Введите пароль...',
        'autocomplete': 'new-password'
    }))

    class Meta:
        model = User
        fields = 'username', 'password'

    def clean_username(self):
        return self.cleaned_data.get('username').strip().lower()


class EmailConfirmationForm(forms.Form):
    email = forms.CharField(
        required=True,
        widget=(forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'введите e-mail...'
        })),
        label='Адрес электронной почты'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует.')
        return email