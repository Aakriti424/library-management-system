"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterApiView.as_view(), name='Register'),
    path('login/', login, name='Login'),
    path('book/', BookApiView.as_view(), name='Book'),
    path('bookid/<int:pk>/', BookIdApi.as_view(), name='Bookid'),
    path('borrowingrecord/', BorrowingRecordApiView.as_view(),name='BorrowingRecord'),
    path('borrowingrecordid/<int:pk>/', BorrowingRecordIdApiView.as_view(), name='BorrowingRecordId')
]
