from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

#class AdminForm(UserCreationForm):
 #   class Meta:
  #      model = User
   #     fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class TaskForm(forms.ModelForm):
    title= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Add new task...'}))
    class Meta:
        model = Task
        fields = '__all__'
        
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
class AddCustomerForm(ModelForm):
    #customername = forms.CharField(label='Customer Name', widget=forms.TextInput(attrs={"placeholder":"Enter Customer Name"}))
    #customeremail = forms.EmailField(label='Customer Email', widget=forms.EmailInput(attrs={"placeholder":"Enter Customer Email"}))
    #customerphone = forms.IntegerField(label='Customer Phone', widget=forms.TextInput(attrs={"placeholder":"Enter Customer Phone"}))
    class Meta:
        model = Customer
        fields = '__all__'
        
class InvoiceForm(forms.ModelForm):
    ProductName = forms.ModelMultipleChoiceField(label='Product Name', queryset=Product.objects.all(),widget=forms.SelectMultiple(attrs={'id': 'id_product_name'}),required=True)
    class Meta:
        model = Retail
        fields = '__all__' 
        exclude = ['product']