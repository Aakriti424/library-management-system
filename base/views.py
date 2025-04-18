from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
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