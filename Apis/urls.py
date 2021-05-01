from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('park-a-car',views.park_a_car,name = 'park_a_car'),
]

