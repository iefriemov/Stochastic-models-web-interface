from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'predict-home'),
    path('model1/', views.index, name = 'predict-model1'),
    ]   