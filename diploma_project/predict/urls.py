from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name = 'predict-home'),
    path('Vasicek_model/', views.Vasicek_model, name = 'predict-Vasicek_model'),
    path('CIR_model/', views.CIR_model, name = 'predict-CIR_model'),
    path('Rendleman_Bartter_model/', views.Rendleman_Bartter_model, name = 'predict-Rendleman_Bartter_model'),
    path('csv/', views.process_csv_file, name = 'predict-csv'),
    path('stoch_model/', views.stoch_model, name = 'predict-stoch_model'),
    ]   

urlpatterns += staticfiles_urlpatterns()