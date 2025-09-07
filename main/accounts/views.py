from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User , OTP
from .serializers import UserSerializer , UserRegisterSerializer , OTPVerifySerializer
from utils.service import send_otp_code
from django.shortcuts import get_object_or_404 , get_list_or_404

# Create your views here.

from django.http import JsonResponse
from django.contrib.auth import get_user_model


class UserRegister (APIView):
    '''
    این ویو برای ثبت‌نام کاربر جدید است. شماره تلفن را دریافت می‌کند و کد OTP را به آن ارسال می‌کند.
    شماره تلفن باید با الگوی 09 شروع شود و 11 رقم باشد. اگر شماره تلفن معتبر باشد، کد OTP به آن ارسال می‌شود.
    '''
    serializer_class = UserRegisterSerializer

    def post (self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        phone_number = serializer.validated_data['phone_number']
        try:
            code = OTP.objects.create_otp_code(phone_number)
            send_otp_code(phone_number, code)
            return Response({"message": "کد OTP به شماره تلفن شما ارسال شد."}, status=200)
        except Exception:
            return Response({"error": "خطا در ارسال کد OTP."}, status=500)



class OTPVerify (APIView):
    '''
    این ویو برای تایید کد OTP است. شماره تلفن و کد OTP را دریافت می‌کند و اگر کد معتبر باشد، کاربر را احراز هویت می‌کند.
    اگر کاربر با این شماره تلفن وجود نداشته باشد، یک کاربر جدید ایجاد می‌کند و توکن JWT را برمی‌گرداند.
    '''
    serializer_class = OTPVerifySerializer

    def post (self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        phone_number = serializer.validated_data.get('phone_number')
        code = serializer.validated_data.get('code')
        if not phone_number or not code:
            return Response({"error": "شماره تلفن و کد OTP الزامی است."}, status=400)
        
        otp = get_object_or_404(OTP, phone_number=phone_number)
        if otp.verify_code(code):
            try:
                user, created = User.objects.update_or_create(
                    phone_number=phone_number,
                )
                token = user.take_jwt_token  
                otp.delete()
                return Response({
                    "token": token,
                    "created": created
                }, status=200)
            except Exception as e:
                return Response({"error": "خطا در ساخت یا دریافت کاربر."}, status=500)
        else:
            return Response({"error": "کد OTP نامعتبر است."}, status=400)
