from .views import LoginAPI, RegisterAPI, ProductViews
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/create-product/', ProductViews.as_view(), name='create-product'),
    path('api/get-product/', ProductViews.as_view(), name='get-product')
]