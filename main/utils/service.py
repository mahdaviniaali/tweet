
import logging
from django.core.mail import send_mail
from django.conf import settings

def send_otp_code(phone, code):
    """
    تابع برای ارسال کد OTP به شماره تلفن
    اینجا باید کد واقعی ارسال پیامک را قرار دهید
    """
    if phone:
        subject = 'کد تأیید شما'
        message = f'کد تأیید شما: {code}\nاین کد تا 5 دقیقه معتبر است.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [phone]
        logging.info(f"OTP code sent: {code}") 
        send_mail(subject, message, from_email, recipient_list)
        return code
    

def send_post_as_email(to_email, subject, message):
    """
    تابع برای ارسال پست به ایمیل
    """
    if to_email:
        logging.info(f"Email sent to {to_email} | Subject: {subject} | Message: {message}")  
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [to_email]
        send_mail(subject, message, from_email, recipient_list)
        return True
    return False