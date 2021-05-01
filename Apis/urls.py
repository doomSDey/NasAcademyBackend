from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('park-a-car',views.park_a_car,name = 'park_a_car'),
    path('unpark-a-car',views.unpark_a_car,name = 'unpark_a_car'),
    path('get-car-or-slot-info',views.get_car_or_slot_info,name = 'get_car_or_slot_info'),
    path('show-table',views.show_table,name = 'show_table'),
]

