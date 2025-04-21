from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import status
from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter



class RegisterApiView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializers = self.get_serializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user = serializers.save()
            group, _ = Group.objects.get_or_create(name=user.role.capitalize())
            user.groups.clear()
            user.groups.add(group)
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
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['genre']
    search_fields = ['title', 'author', 'genre']

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset()) 
        page=self.paginate_queryset(queryset)
        if page is not None:
            serializer=self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializers=self.get_serializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=400)
    


class BookIdApi(GenericAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[IsAuthenticated, DjangoModelPermissions]
    
    def put(self, request, pk):
        instance=self.get_object()
        self.filter_queryset
        serializers=self.get_serializer(instance, request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=200)
        return Response(serializers.errors, status=400)
    
    def delete(self, request, pk):
        instance=self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BorrowingRecordApiView(GenericAPIView):
    queryset = BorrowingRecord.objects.all()
    serializer_class = BorrowingRecordSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['borrower']

    def get(self, request):
        if request.user.role=="librarian":
            model=self.get_queryset()
            filtered_queryset = self.filter_queryset(model) 
            page=self.paginate_queryset(filtered_queryset)

            if page is not None:
                serializer=self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(filtered_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        user=BorrowingRecord.objects.filter(borrower=request.user)
        serializer=self.get_serializer(user, many=True)
        return Response(serializer.data, status=200)
    


    def post(self, request):
        borrowed_book = request.data.get('borrowed_book')
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if BorrowingRecord.objects.filter(borrower=request.user, borrowed_book=borrowed_book).exists():
                return Response({'error': 'You cannot borrow the same book twice'}, status=status.HTTP_403_FORBIDDEN)

            current_borrow_count = BorrowingRecord.objects.filter(borrower=request.user).count()
            if current_borrow_count >= 5:
                return Response({'error': 'You cannot borrow more than 5 books'}, status=status.HTTP_403_FORBIDDEN)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BorrowingRecordIdApiView(GenericAPIView):
    queryset=BorrowingRecord.objects.all()
    serializer_class=BorrowingRecordSerializer
    permission_classes=[IsAuthenticated, DjangoModelPermissions]

    def put(self, request, pk):
        instance=self.get_object()
        serializers=self.get_serializer(instance, request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=200)
        return Response(serializers.errors, status=400)
    
    def delete(self, request, pk):
        instance=self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)