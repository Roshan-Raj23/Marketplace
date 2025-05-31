from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Product , OrderDetail
from .forms import OrderDetailForm , ProductForm , UserRegistrationForm
import datetime

def index(request):
    products = Product.objects.all()
    return render(request , 'myapp/index.html' , {'products': products})

def product_detail(request, product_id):    
    product = Product.objects.get(id=product_id)
    if (request.method == 'POST'):
        form = OrderDetailForm(request.POST or None)
        if (form.is_valid()):
            # user = request.user
            # print("The data is : " , form.cleaned_data.get('quantity'))
            if (request.user.id == None):
                return redirect('myapp:login')
            
            order = OrderDetail()
            order.product = product
            order.customer_email = request.user.email
            order.quantity = form.cleaned_data.get('quantity')
            order.amount = order.quantity * product.price
            order.has_paid = True
            order.save()
            
            product.total_orders += 1
            product.total_sales_amount += order.amount
            product.save()
            
            return redirect("myapp:after_order" , order_id=order.id)
        
    form = OrderDetailForm()
    return render(request, 'myapp/product_detail.html', {'product': product , 'form': form})

def after_order(request , order_id):
    order = OrderDetail.objects.get(id=order_id)
    return render(request , 'myapp/success.html' , {'order':order})

@login_required
def create_product(request):
    if (request.method == 'POST'):
        product = ProductForm(request.POST , request.FILES)
        if (product.is_valid()):
            new_product = product.save(commit=False)
            new_product.seller = request.user
            new_product.save()
            return redirect('myapp:index')
    
    product_form = ProductForm()
    return render(request , 'myapp/create_product_form.html' , {'product_form' : product_form})

@login_required
def update_product(request , product_id):
    product = Product.objects.get(id = product_id)
    if product.seller != request.user:
        return redirect('myapp:invalid')
    
    product_form = ProductForm(request.POST or None , request.FILES or None , instance=product)
    if (request.method == 'POST'):
        if (product_form.is_valid()):
            product_form.save()
            return redirect('myapp:index')
    
    return render(request , 'myapp/update_product_form.html' , {'product_form' : product_form , 'product_id' : product_id})

@login_required
def delete_product(request , product_id):    
    product = Product.objects.get(id=product_id)
    if product.seller != request.user:
        return redirect('myapp:invalid')
    
    if (request.method == 'POST'):
        product.delete()
        return redirect('myapp:index')
    
    return render(request , 'myapp/confirm_delete.html' , {'product' : product})

@login_required
def dashboard(request):
    products = Product.objects.filter(seller = request.user)
    return render(request , 'myapp/dashboard.html' , {'products' : products})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        user_form.save()
        return redirect('myapp:login')
    
    user_form = UserRegistrationForm()
    return render(request , 'myapp/register.html' , {'user_form': user_form})

def invalid(request):
    return render(request , 'myapp/invalid.html')

@login_required
def my_purchases(request):    
    orders = OrderDetail.objects.filter(customer_email= request.user.email)
    return render(request , 'myapp/my_purchases.html' , {'orders': orders})

@login_required
def sales(request):    
    orders = OrderDetail.objects.filter(product__seller=request.user)
    total_sales = {}
    total_sales['total'] = orders.aggregate(Sum('amount'))
    
    lst = [[7 , 'weekly'] , [30 , 'monthly'] , [365 , 'yearly']]
    for item in lst:
        var = datetime.date.today() - datetime.timedelta(item[0])
        orders = OrderDetail.objects.filter(product__seller=request.user , created_on__gt=var)
        total_sales[item[1]] = orders.aggregate(Sum('amount'))
        
    
    
    # Everyday sum for the past 30 days
    daily_sales_sums = OrderDetail.objects.filter(product__seller=request.user).values('created_on__date').order_by('created_on__date').annotate(sum = Sum('amount'))
    
    product_sales_sums = OrderDetail.objects.filter(product__seller=request.user).values('product__name').order_by('-amount').annotate(sum = Sum('amount'))
    
    
    
    context = {
        'total_sales' : total_sales,
        'daily_sales_sums' : daily_sales_sums,
        'product_sales_sums' : product_sales_sums,
    }
    
    return render(request , 'myapp/sales.html' , context)



