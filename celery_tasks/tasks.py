__author__ = 'Administrator'

from django.core.mail import send_mail
from django.conf import settings
from django.template import loader, RequestContext
from celery import Celery
import time

# 在任务处理者一端加这几句
import os

# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()

from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
from django_redis import get_redis_connection

app = Celery('celery_tasks.tasks', broker='redis://172.16.179.142:6379/8')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """
    发送激活邮件
    :param to_email:
    :param username:
    :param token:
    :return:
    """
    subject = 'Welcome to join daily fresh system'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
    username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)

    time.sleep(5)

@app.task
def generate_static_index_html():
    """
    产生首页静态页面
    :return:
    """
    # get the goods type
    types = GoodsType.objects.all()
    # get the banner image of the index page
    goods_banners = IndexGoodsBanner.objects.all()
    # get the promotion info
    promotion_banners = IndexPromotionBanner.objects.all()

    for type in types:
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type = type,display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type = type,display_type=0).order_by('index')
        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners

    # 组织模板上下文
    context = {
        'type':types,
        'goods_banners':goods_banners,
        'promotion_banners':promotion_banners
    }
    # 1.加载模板文件,返回模板对象

    temp = loader.get_template('static_index.html')
       # 2.模板渲染
    static_index_html = temp.render(context)

    save_path = os.path.join(settings.BASE_DIR,'static')
    with open(save_path,'w') as f:
        f.write(static_index_html)




