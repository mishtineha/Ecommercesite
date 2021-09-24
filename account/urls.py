from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
    # path('', views.index, name='index'),
    url(r'sign-in/', views.LoginPage.as_view(), name='signin'),
    url(r'^password/$', views.profile, name='change_password'),
    url('sign-up', views.signup, name='signup'),
    url('dashboard', views.profile, name='profile'),
    # path('resendOTP', resend_otp),
    url('send-otp/', views.send_otp, name='send_otp')
    # url(r'^settings/$', core_views.settings, name='settings'),
    # url(r'^settings/password/$', core_views.password, name='password'),
]
