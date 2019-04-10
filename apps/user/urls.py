__author__ = 'Administrator'

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from user.views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView, AddressView, UserOrderView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register')
    , url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active')
    , url(r'^login$', LoginView.as_view(), name='login')
    , url(r'^logout$', LoginView.as_view(), name='logout')

    , url(r'^$', UserInfoView.as_view(), name='user')
    , url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order')
    , url(r'^address$', AddressView.as_view(), name='address')

]
