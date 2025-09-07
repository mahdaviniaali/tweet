from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager, OTPManager
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken 
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _  

# Create your models here.
class User(AbstractBaseUser):
    # اطلاعات پایه
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # وضعیت
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_verified = models.BooleanField(default=False)  
    # زمان‌بندی
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    tags = TaggableManager(blank=True, verbose_name=_("تگ ها"))
    following = models.ManyToManyField("self", through="interactions.Follow", symmetrical=False, related_name="followers")
    objects = UserManager() 

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.phone_number
    
    @property
    def take_jwt_token(self):
        '''تولید توکن JWT برای کاربر'''
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
       


# otp code برای احراز هویت دو مرحله‌ای
class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=5)
    expires_at = models.DateTimeField()
    objects = OTPManager()
    
    def is_valid(self):
        return timezone.now() < self.expires_at

    @staticmethod
    def is_valid_for_user(phone_number):
        return OTP.objects.filter(phone_number=phone_number, expires_at__gt=timezone.now()).exists()


    def verify_code( self, code):
        if self.code == code and self.is_valid():
            return True
        return False

    def __str__(self):
        return f"{self.phone_number} - {self.code}"

    class Meta:
        ordering = ['-expires_at']





