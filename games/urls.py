from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),   
    path('login/', views.login, name='login'),
    path('investment/', views.investment, name='investment'),
    path('investmentSubmit/', views.investmentSubmit, name='investmentSubmit'),
    path('returnedSubmit/', views.returnedSubmit, name='returnedSubmit'),
    path('final/', views.final, name='final'),
    path('returning/', views.returned, name='returned'),
    path('compare/', views.compare, name='compare'),
    path('question/', views.question, name='question'),
    path('record/', views.record, name='record')

    # path('', views.p, name='welcome'),    
]
