from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from django.contrib.auth.models import User
from rest_framework import viewsets
from . import serializers, models
from rest_framework.response import Response
import calendar
import datetime
from datetime import date, timedelta
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import base64
from django.core.mail import send_mail
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from django.conf import settings



class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

class SendVerifyCode(object):
    @staticmethod
    def send_email_code(code,to_email_adress):
        try:
            success_num = send_mail(subject='Login OTP Redseer', message=f' Your verification code is 【{code}】. If I do not operate , Please ignore .',from_email='shahzma@redseerconsulting.com',recipient_list = ['shahzmaalif@gmail.com'], fail_silently=False)
            return success_num
        except:
            return 0



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


# CAN CREATE OR UPDATE OTP IN USER MODEL
class LoginApi(CreateAPIView):
    
    # get otp  and send it to user when he clicks submit
    def get(self, request):
        OTP = 2704
        print(OTP)
        # email = serializer.validated_data["email"]
        email = request.data.get('email')
        send_mail(subject='Login OTP Redseer', message=f' Your verification code is 【{OTP}】. If I do not operate , Please ignore .',from_email=settings.EMAIL_HOST_USER,recipient_list = ['shahzma@redseerconsulting.com'], fail_silently=False)
        # send OTP to user
        sms_status = SendVerifyCode.send_email_code(code=OTP, to_email_adress=email)
        if sms_status == 0:
        # Log
            return Response({"msg": " Failed to send mail "}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # code_record = VerifyCode(code=code, email=email)
            # Save verification code
            # code_record.save()
            return Response({"msg": f" The verification code has been sent to {email} Send complete .OTP = {OTP}"}, status=status.HTTP_201_CREATED)

    # This Method verifies the OTP
    def post(self, request):
        OTP = request.data.get('OTP')
        print(OTP)
        username = request.data["username"]
        user = User.objects.get(username=username)
        # verify OTP and email and pass
        if OTP == 2704:
            token = Token.objects.get(user=user)
            return Response({'token': token.key})
            # return Response({"msg": " Success "}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": " Failed "}, status=status.HTTP_400_BAD_REQUEST)