from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null = True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (('Indoor', 'Indoor'), ('Outdoor', 'Outdoor'))
    tags = models.ManyToManyField(Tag)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    product_id = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    CITY = (('Delhi', 'Delhi'), ('London', 'London'), ('Berlin', 'Berlin'), ('Amsterdam', 'Amsterdam'), ('Istanbul', 'Istanbul'), ('Montreal', 'Montreal'), ('Toronto', 'Toronto'))
    customer = models.ForeignKey(Customer, null = True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)
    city = models.CharField(max_length=200, null=True, choices=CITY)
    STATUS = (('Pending', 'Pending'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    def __str__(self):
        return self.product.name
        
class Retail(models.Model):
    CITYO = (('Delhi', 'Delhi'), ('London', 'London'), ('Berlin', 'Berlin'), ('Amsterdam', 'Amsterdam'), ('Istanbul', 'Istanbul'), ('Montreal', 'Montreal'), ('Toronto', 'Toronto'))
    customer = models.ForeignKey(Customer, null = True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)
    cityo = models.CharField(max_length=200, null=True, choices=CITYO)
    def __str__(self):
        return self.product.name
        
class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title