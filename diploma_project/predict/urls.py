from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name = 'predict-home'),
    path('model1/', views.index, name = 'predict-model1'),
    path('csv/', views.process_csv_file, name = 'predict-csv'),
    ]   

urlpatterns += staticfiles_urlpatterns()