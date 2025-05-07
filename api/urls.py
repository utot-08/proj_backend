from django.urls import path
from .views import (
    owner_list, owner_detail,
    firearm_list, firearm_detail,
    owner_firearms
)

urlpatterns = [
    # Owner endpoints
    path('owners/', owner_list, name='owner-list'),
    path('owners/<str:full_legal_name>/', owner_detail, name='owner-detail'),
    
    # Firearm endpoints
    path('firearms/', firearm_list, name='firearm-list'),
    path('firearms/<str:serial_number>/', firearm_detail, name='firearm-detail'),
    
    # Get all firearms for a specific owner
    path('owners/<str:owner_name>/firearms/', owner_firearms, name='owner-firearms'),
]