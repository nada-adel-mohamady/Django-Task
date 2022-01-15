from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .serializers import UserSerializer, RegisterSerializer, ProductSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework import status
from .models import Product
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')

class ProductViews(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller_id=request.user.id)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user_id = request.user.id
        products = Product.objects.filter(seller=user_id).order_by('price')
        serializer = ProductSerializer(products, many=True)
        
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
