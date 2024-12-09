"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.urls import path, include
from app.cons_handler import LiveScrapView
from  live_control.views import adx_amount
from app import game_man

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/<str:ckey>/check-ip/',views.check_ip,name='check user'),
    path('',views.def_page,name='def_page'),
    #win_management
    path('manage-betslips/<str:key>/', views.manage_bets_secure, name='manage_bets_secure'),
    #path('manage-betslips/<str:ckey>/', views.manage_betslips, name='manage_betslips'),
    path('manage-wins/<str:ckey>/', views.manage_wins, name='manage_wins'),
    #manage game mod
    path('manage/<str:ckey>/', game_man.manage_game, name='manage_game'),
    path('malic/',views.malic,name='def_page'),
    path('slip/',views.process_slip,name='process_slip'),
    path('register_page/',views.register_page,name='register_page'),
    path('login_page/',views.login_page,name='login_page'),
    path('login_page/login/',views.login,name='login'),
    path('register_page/register/login/',views.login,name='login'),
    path('register_page/register/',views.register,name='register'),
    path('home/<str:ckey>/',views.home_page,name='home_page'),
    path('pending/<str:ckey>/', views.pending, name='pending_func'),  
    path('api/live-scrap/', LiveScrapView.as_view(), name='live_scrap'),
    path('success/',views.success,name='success_slip'),
    path('fail/',views.fail_slip,name='fail_slip'),
    path('pay_mpesa/<str:amount>/<str:ckey>/', views.mpesa_deposit, name='mpesa_func'),
    path('live-scores/', views.live_data, name='live_scores'),
    path('finance/<str:ckey>/', views.finance_page, name='finance'),
    path('profile/<str:ckey>/', views.client_profile, name='profile'),
    path('mpesa-withdraw/', views.mpesa_withdraw, name='mpesa_withdraw'),
    path('transac-status/', views.mpesa_response, name='mpesa_response'),
    path('', include('live_control.urls')),
    path('home/<str:ckey>/control/', include('live_control.urls')),
    #manual payment
    path('home/<str:ckey>/pay/',include('payment_int.urls')),
    #add amount manually
    path('update-amount/', adx_amount),
    #about
    path('about/',views.about),
    #customer support
    path('chat/',views.chatx),
    path('generate-referral/', views.generate_referral, name='generate_referral'),
    #refer program
    path('referral/<str:referral_code>/', views.referral_page, name='referral_page'),
    path('view-referrals/', views.view_referrals, name='view_referrals'),
]
