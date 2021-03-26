from django.urls import path
from . import views

urlpatterns = [
    path('couriers', views.upload_couriers)
]