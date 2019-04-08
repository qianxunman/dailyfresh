from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.conf import settings

from user.models import  User,Address
from goods.models import GoodsSKU
from order.models import OrderInfo,OrderGoods

from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer,Serializer
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
import re
import time

# Create your views here.


class RegisterView(View):
    """
    register
    """
    def get(self,request):
        return render(request,'register.html')

    def post(self, request):
        """
        solve the request data
        :param request:
        :return:
        """
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        if not all([username,password,email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = None
        if user :
            return render(request,'register.html',{'errmsg':'the user has be registered'})
        # really register
        user = User.objects.create_user(username,email,password)
        user.is_active = 0
        user.save()

        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()

        send_register_active_email.delay(email,username,token)
        return HttpResponse(b'ok',content_type='text/html')


