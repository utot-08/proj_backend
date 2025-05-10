from django.urls import path
from .views import (
    owner_list, owner_detail,
    firearm_list, firearm_detail,
    owner_firearms,
    user_list, user_detail, update_firearm_status, owner_detail_by_id, get_owner_by_id
)

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    # Owner endpoints
    path('owners/', owner_list, name='owner-list'),
    path('owners/<str:full_legal_name>/', owner_detail, name='owner-detail'),
    path('owners/<int:pk>/', get_owner_by_id, name='get-owner-by-id'),
    
    
    # Firearm endpoints
    path('firearms/', firearm_list, name='firearm-list'),
    path('firearms/<str:serial_number>/', firearm_detail, name='firearm-detail'),
    path('firearms/<str:serial_number>/status/', update_firearm_status),  # New endpoint
    
    # Get all firearms for a specific owner
    path('owners/<str:owner_name>/firearms/', owner_firearms, name='owner-firearms'),

    path('owners/by-id/<int:pk>/', owner_detail_by_id, name='owner-detail-by-id'),
]