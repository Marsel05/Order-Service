from django.urls import path
from .views import *

urlpatterns = [
    path('api/orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name="order_list"),
    path('api/orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="order_detail"),
]
