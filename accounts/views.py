from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from .forms import AdminForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def Home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = Order.objects.count()
    delivered = Order.objects.filter(status = 'Delivered').count()
    pending = Order.objects.filter(status = 'Pending').count()
    return render(request, 'accounts/dashboard.html', {'total_orders':total_orders, 'delivered':delivered, 'pending':pending, 'customers':customers, 'orders':orders})

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

def Customers(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    orders_count = order.count()
    return render(request, 'accounts/customer.html', {'customer':customer, 'order':order, 'orders_count':orders_count})

def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        form.save()
        return redirect('/')
    return render(request, 'accounts/order_form.html', {'form':form})

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        form.save()
        return redirect('/')
    return render(request, 'accounts/order_form.html', {'form':form})

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', {'item':order})

def termsofServices(request):
    return render(request, 'accounts/termsofservices.html')

def updateCustomer(request, pk):
    updatecustomer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        namenew = request.POST.get('newname') 
        emailnew = request.POST.get('newemail')
        phonenonew = request.POST.get('newphoneno')
        updatecustomer.name = namenew
        updatecustomer.email = emailnew
        updatecustomer.phone = phonenonew
        updatecustomer.save()
        return redirect('/')
    return render(request, 'accounts/updatecustomer.html', {'item':updatecustomer})

def deleteCustomer(request, pk):
    deletecustomer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        deletecustomer.delete()
        return redirect('/')
    return render(request, 'accounts/deletecustomer.html', {'deletecustomer':deletecustomer})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is Incorrect')
    return render(request, 'accounts/login.html', {'user':request.user})

def register(request):
    form = AdminForm()
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was suucessfully created for' + user )
            return redirect('login')
    return render(request, 'accounts/register.html', {'form':form, 'user':request.user})

def logoutUser(request):
    logout(request)
    return redirect('login')



