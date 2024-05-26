from django.urls import path

from .views import *

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/api/check_email/', CheckUserEmail.as_view(), name='check_email'),
    path('registration/api/confirm_email/', ConfirmUserEmail.as_view(), name='confirm_email'),
    path('confirmation_email/', logout_view, name='confirm_email'),
    path('registration/api/send_activation_code/', SendActivationCode.as_view(), name='send_activation_code'),
]