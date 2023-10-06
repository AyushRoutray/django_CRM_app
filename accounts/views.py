from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from .forms import UserRegisterForm
from .forms import TaskForm
from .forms import AddProductForm
from .forms import AddCustomerForm
from .forms import InvoiceForm
from .filters import OrderFilter
from .filters import ProductFilter
from .filters import CustomerFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from guest_user.decorators import allow_guest_user
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ColorBar
from bokeh.models.annotations import Label
from bokeh.transform import linear_cmap
from math import pi, tan, log
from django.db.models import Count, Q
from bokeh.palettes import Viridis5, Viridis256
from django.views import View
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
import pandas as pd
from bokeh.models import ColumnDataSource, FactorRange
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.forms import formset_factory
from django.http import QueryDict
# Create your views here.
def Home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = Order.objects.count()
    common_customers = Customer.objects.filter(Q(order__isnull=False) & Q(retail__isnull=False)).distinct()[:5]
    common_products = Product.objects.filter(Q(order__isnull=False) & Q(retail__isnull=False)).distinct()[:5]
    delivered = Order.objects.filter(status = 'Delivered').count()
    pending = Order.objects.filter(status = 'Pending').count()
    out_for_delivery = Order.objects.filter(status = 'Out for Delivery').count()
    tag_counts = Tag.objects.annotate(total_count=Count('product__order') + Count('product__retail')).order_by('-total_count')
    tags = []
    num = []
    legend = ['Electronics', 'Sports', 'Clothing', 'Home Applicances', 'Accessories']
    for tag_count in tag_counts:
        tags.append(tag_count.name)
        num.append(tag_count.total_count)
    total_orders = Order.objects.count()
    total_sales = Retail.objects.count()
    x = {'Online': total_orders, 'Retail': total_sales,}
    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    colors = ['#8A2BE2', '#FFFF00']
    color = Viridis5
    data['color'] = colors
    p = figure(width=500, height=400, title="Pie Chart", toolbar_location=None, tools="hover", x_range=(-0.5, 1.0), background_fill_color="#1d2634", tooltips="@value")
    p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)
    p.toolbar_location = None
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    plot = figure(x_range=tags, width=500, height=400, y_range=(0, max(num) * 1.2), background_fill_color="#1d2634")
    mapper = linear_cmap(field_name='num', palette=Viridis256, low=min(num), high=max(num))
    plot.vbar(x=tags, top=num, width=0.5, color=color, line_color="grey", line_width=2, legend_label="tags")
    plot.xgrid.grid_line_color = None
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0, 0), title="Values")
    plot.y_range.start = 0
    plot.toolbar_location = None
    plot.legend.location = "top_right"
    plot.legend.click_policy="hide"
    plot.title.text_font_size = "18pt"  # Title font size
    plot.axis.axis_label_text_font_style = "bold"  # Axis label font style
    plot.add_layout(color_bar, 'right')
    plot.yaxis.axis_label = "Count"
    plot.axis.major_label_text_font_size = "8pt"
    cityo = Order.objects.values_list('city', flat=True)
    cityr = Retail.objects.values_list('cityo', flat=True)
    k = 6378137
    Delhi = {
        "latitude" : 28.6139,
        "longitude" : 77.2090
        }
    London = {
        "latitude" : 51.5074,
        "longitude" : -0.1278
        }
    Berlin = {
        "latitude" : 52.5200,
        "longitude" : 13.4050
    }
    Amsterdam = {
        "latitude" : 52.3792,
        "longitude" : 4.8994
    }
    Istanbul = {
        "latitude" : 41.0082,
        "longitude" : 28.9784
    }
    Montreal = {
        "latitude" : 45.5017,
        "longitude" : -73.5673
    }
    Toronto = {
        "latitude" : 43.651070,
        "longitude" : -79.347015
    }
    cities = {
        "Delhi" : Delhi,
        "London" : London,
        "Berlin" : Berlin,
        "Amsterdam" : Amsterdam,
        "Istanbul" : Istanbul,
        "Montreal" : Montreal,
        "Toronto" : Toronto
    }
    plot1 = figure(width=500, height=400, x_range=(-12000000, 9000000), y_range=(-1000000, 7000000), x_axis_type='mercator', y_axis_type='mercator')
    plot1.add_tile("Esri World Imagery", retina=True)
    plot1.toolbar_location = None
    plot1.axis.visible = False
    for cityo in cityo:
        x = float(cities[cityo]["longitude"]) * (k * pi/180.0)
        y = log(tan((90 + float(cities[cityo]["latitude"])) * pi/360.0)) * k
        plot1.circle(x,y,size=10,color="yellow", legend_label="Online")
    for cityr in cityr:
        x = float(cities[cityr]["longitude"]) * (k * pi/180.0)
        y = log(tan((90 + float(cities[cityr]["latitude"])) * pi/360.0)) * k
        plot1.dash(x,y,size=15,color="blue", legend_label="Retail")
    plot1.legend.click_policy="hide"
    pname = Product.objects.values_list('name', flat=True)
    pprice = Product.objects.values_list('price', flat=True)
    dataname = list(pname)
    dataprice = list(pprice)
    source = ColumnDataSource(data=dict(product_names=dataname, product_prices=dataprice))
    x_range = FactorRange(factors=tuple(dataname))
    plot2 = figure(width=500, height=400, x_range=x_range, tooltips="@product_names:@product_prices")
    plot2.scatter(x='product_names', y='product_prices', source=source, size=3, color="navy")
    plot2.line(x='product_names', y='product_prices', source=source, color="purple")
    plot2.toolbar_location = None
    script2, div2 = components(plot1)
    script, div = components(p)
    script1, div1 = components(plot)
    script3, div3 = components(plot2)
    return render(request, 'accounts/dashboard.html', {'total_orders':total_orders, 'delivered':delivered, 'pending':pending, 'customers':customers, 'orders':orders, 'out_for_delivery':out_for_delivery, 'script':script, 'div':div, 'script1':script1, 'div1':div1, 'script2':script2, 'div2':div2, 'script3':script3, 'div3':div3, 'common_customers':common_customers, 'common_products':common_products})

def customert(request):
    customer = Customer.objects.all()
    form = AddCustomerForm()
    myFilter = CustomerFilter(request.GET, queryset=customer)
    customer = myFilter.qs
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        form.save()
        return redirect('customert')
    return render(request, 'accounts/customertable.html', {'customert':customer, 'form':form, 'myFilter':myFilter})

def products(request):
    formaddproduct = AddProductForm()
    products = Product.objects.all()
    tags = Product.objects.all().prefetch_related('tags')
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    if request.method == 'POST':
        formaddproduct = AddProductForm(request.POST)
        if formaddproduct.is_valid():
            formaddproduct.save()
        return redirect('products')
    return render(request, 'accounts/products.html', {'products':products, 'tags':tags, 'formaddproduct':formaddproduct, 'myFilter':myFilter})

def Customers(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    orders_count = order.count()
    if request.method == 'POST':
        namenew = request.POST.get('newname') 
        emailnew = request.POST.get('newemail')
        phonenonew = request.POST.get('newphoneno')
        customer.name = namenew
        customer.email = emailnew
        customer.phone = phonenonew
        customer.save()
        return redirect('/')
    return render(request, 'accounts/customer.html', {'customer':customer, 'order':order, 'orders_count':orders_count, 'item':customer})

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
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was suucessfully created for' + user )
            return redirect('login')
    return render(request, 'accounts/register.html', {'form':form, 'user':request.user})

def logoutUser(request):
    logout(request)
    return redirect('Home')

@allow_guest_user    
def guest(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was suucessfully created for' + user )
            return redirect('login')
    return render(request, 'accounts/dashboard.html', {'form':form, 'user':request.user})

def barcode(request):
    products = Product.objects.all()
    tags = Product.objects.all().prefetch_related('tags')
    return render(request, 'accounts/barcode.html', {'products':products, 'tags':tags})
    
def pikosheets(request):
    return render(request, 'accounts/pikosheets.html')
    
def todo(request):
    tasks = Task.objects.all()
    #task = Task.objects.get(id=pk)
    form = TaskForm()
    #form1 = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('todo')
    context = {'tasks':tasks, 'form':form}
    return render(request, 'accounts/todo.html', context)
    
def udtodo(request, pk):
    task = Task.objects.get(id=pk)
    form1 = TaskForm(instance=task)
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        if 'form1_submit' in request.POST:
            form1 = TaskForm(request.POST, instance=task)
            if form1.is_valid():
                form1.save()
                return redirect('todo')
        else:
            item.delete()
            return redirect('todo')   
    context = {'form1':form1, 'item':item}
    return render(request, 'accounts/udtodo.html', context)
    
def invoice(request):
    form_data = None

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer']
            cityo = form.cleaned_data['cityo']
            selected_products = request.POST.getlist('id_product_name')

            request.session['invoice-form-data'] = {
                'customer_id': customer_name.id,
                'cityo': cityo,
                'selected_products': selected_products,
            }
            form_data = request.session['invoice-form-data']

    else:
        form = InvoiceForm()
        #form_data = request.session.get('invoice-form-data', None)

    if form_data is not None:
        customer_id = form_data['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        template = get_template('accounts/template.html')
        context = {
            'customer_name':  customer.name,
            'cityo': form_data['cityo'],
            'selected_products': form_data.get('selected_products', []), 
        }
        html_content = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html.escape(html_content) + '</pre>')
        return response
    return render(request, 'accounts/invoice.html', {'form':form})
    
def orderstatus(request):
    orders = Order.objects.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        form.save()
        return redirect('orderstatus')
    return render(request, 'accounts/orderstatus.html', {'orders':orders, 'form':form, 'myFilter':myFilter})
    
def support(request):
    return render(request, 'accounts/support.html')

def template(request):
    return render(request, 'accounts/template.html')

