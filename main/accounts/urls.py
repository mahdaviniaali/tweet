from django.urls import path
from . import views

app_name = 'accounts'
# accounts/create-superuser
urlpatterns = [
   path('register/', views.UserRegister.as_view(), name='user_register'),
   path('verify/', views.OTPVerify.as_view(), name='otp_verify'),
]
