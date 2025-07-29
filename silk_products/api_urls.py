from django.urls import path
from . import api_views

urlpatterns = [
    path('register/', api_views.register_user, name='api_register'),
    path('profile/', api_views.user_profile, name='api_profile'),
    path('logout/', api_views.logout_user, name='api_logout'),
    path('products/', api_views.SilkProductListCreateAPIView.as_view(), name='api_product_list_create'),
    path('products/<int:pk>/', api_views.SilkProductRetrieveUpdateDestroyAPIView.as_view(), name='api_product_detail'),
    path('products/stats/', api_views.product_stats, name='api_product_stats'),
]