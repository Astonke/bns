from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.start, name='start-page'),
    path('dash',views.pay_options),
    path('proof',views.proof),
]

