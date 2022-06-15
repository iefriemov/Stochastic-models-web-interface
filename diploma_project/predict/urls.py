from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name = 'predict-home'),
    path('csv/', views.process_csv_file, name = 'predict-csv'),
    path('stoch_model/', views.stoch_model, name = 'predict-stoch_model'),
    path('models_predict/', views.models_predict, name = 'predict-models_predict'),
    path('interests/', views.interests, name = 'predict-interests'),
    ]   

urlpatterns += staticfiles_urlpatterns()