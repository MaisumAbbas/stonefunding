from stonefundingapp import views
from django.urls import path

app_name = 'stonefundingapp'

urlpatterns = [
    path('report/', views.report, name='report'),
    path('user_login/', views.user_login, name='user_login'),
    path('bot/', views.bot, name='bot'),
]