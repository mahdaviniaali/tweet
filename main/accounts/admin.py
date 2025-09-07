from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTP
from django.utils import timezone
# Register your models here.


# ثبت مدل‌ها در ادمین
admin.site.register(User)
admin.site.register(OTP)