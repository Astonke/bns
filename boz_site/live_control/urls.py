# scores/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('main/<str:ckey>',views.main),
    path('live_control/<str:ckey>', views.score_list, name='score_list'),
    path('main/live_control/<str:ckey>', views.score_list, name='score_list'),
    path('up_amount/<str:ckey>', views.up_amount),
    path('main/up_amount/<str:ckey>', views.up_amount),
    
]
