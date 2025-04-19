from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import Group


#USER VIEWS

class RegisterApiView(GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def post(self, request):
        serializers=self.get_serializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user=serializers.save()
            group,_=Group.objects.get_or_create(name=user.role.capitalize())
            return Response(serializers.data, status=201)
        return Response(serializers.errors, status=400)



#LOGIN VIEW 

@api_view(["POST"])

def login(request):
    username=request.data.get('username')
    password=request.data.get('password')
    verify=authenticate(username=username, password=password)
    if verify==None:
        return Response({'invalid': 'Invalid username or password'}, status=403)
    token,_ = Token.objects.get_or_create(user=verify)
    return Response(
        {
            'token': token.key,
            'role' : verify.role
        },
        status=200
    )



#BOOKS API VIEW

class BookApiView(GenericAPIView):
    queryset=Book
    serializer_class=BookSerializer

    def get(self, request):
        instance=self.get_queryset()
        serializers=self.get_serializer(instance, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializers=self.get_serializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user=serializers.save()
            group,_=Group.objects.get_or_create(name=user.role.capitalize())
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=400)
    


class BookIdApi(GenericAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer

    def get(self, request, id):
        instance=self.get_object()
        serializers=self.get_serializer(instance)
        return Response(serializers.data, status=200)
    
    def put(self, request, pk):
        instance=self.get_object()
        serializers=self.get_serializer(instance)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=200)
        return Response(serializers.errors, status=400)
    
    def delete(self, request, pk):
        instance=self.get_object()
        instance.delete()

    
