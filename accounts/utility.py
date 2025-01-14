import random
from django.core.cache import cache
from django.core.mail import send_mail
from captcha.conf import settings


def send_otp(mobile):
    otp = random.randint(1000, 9999)
    cache.set(mobile, otp, 300)
    # send otp with sms service
    print(f'OTP for {mobile}: {otp}')


def send_activation_code(activation_url, email_address):
    send_mail(
        subject='Activate your email',
        message=f'Please click on the link below to activate user account. {activation_url}',
        from_email='admin@admin.com',
        recipient_list=[email_address]
    )


def random_char_challenge():
    chars, ret = "abcdefghjkmnprstuvwxyz23456789", ""
    for i in range(settings.CAPTCHA_LENGTH):
        ret += random.choice(chars)
    return ret.upper(), ret

