from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('history/', views.diagnosis_history, name='diagnosis_history'),
]