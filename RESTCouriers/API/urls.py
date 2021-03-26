from django.urls import path
from . import views

urlpatterns = [
    path('couriers', views.upload_couriers),
    path('couriers/<int:courier_id>', views.update_couriers),
]