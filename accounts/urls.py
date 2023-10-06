from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.Home, name='dashboard'),
    path('customer/<str:pk>/', views.Customers, name = 'customers'),
    path('product/', views.products, name='products'),
    path('createorder/', views.createOrder, name='createorder'),
    path('updateorder/<str:pk>/', views.updateOrder, name='updateorder'),
    path('deleteorder/<str:pk>/', views.deleteOrder, name='deleteorder'),
    path('updatecustomer/<str:pk>/', views.updateCustomer, name='updatecustomer'),
    path('deletecustomer/<str:pk>/', views.deleteCustomer, name='deletecustomer'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('customert/', views.customert, name='customert'),
    path('barcode/', views.barcode, name='barcode'),
    path('pikosheets/', views.pikosheets, name='pikosheets'),
    path('todo/', views.todo, name='todo'),
    path('todo/<str:pk>/', views.udtodo, name='udtodo'),
    path('invoicing/', views.invoice, name='invoice'),
    path('orderstatus/', views.orderstatus, name='orderstatus'),
    path('support/', views.support, name='support'),
    path("convert/", include("guest_user.urls")),
    path('guest/', views.guest, name='guest'),
]
