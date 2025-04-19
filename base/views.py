from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status


#USER VIEWS

class RegisterApiView(GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def post(self, request):
        serializers=self.get_serializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=201)
        return Response(serializers.errors, status=400)
    
@api_view(["POST"])

def login(request):
    username=request.data.get('username')
    password=request.data.get('password')
    verify=authenticate(username=username, password=password)
    if verify==None:
        return Response({'invalid': 'Invalid username or password'}, status=403)
    token,_ = Token.objects.get_or_create(user=verify)
    return Response(token.key, status=200)
