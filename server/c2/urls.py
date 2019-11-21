from django.urls import path
from . import views

urlpatterns = [
    path('client/test', views.clientTest, name='Client_Testing'),
    path('client/<str:uuid>/commands', views.commands, name='Client_Commands'),
]
