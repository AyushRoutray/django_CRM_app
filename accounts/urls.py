from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='dashboard'),
    path('customer/<str:pk>/', views.Customers, name = 'customers'),
    path('product/', views.products, name='products'),
    path('createorder/', views.createOrder, name='createorder'),
    path('updateorder/<str:pk>/', views.updateOrder, name='updateorder'),
    path('deleteorder/<str:pk>/', views.deleteOrder, name='deleteorder'),
    path('termsofservices/', views.termsofServices, name='termsofservices'),
    path('updatecustomer/<str:pk>/', views.updateCustomer, name='updatecustomer'),
    path('deletecustomer/<str:pk>/', views.deleteCustomer, name='deletecustomer'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
]
