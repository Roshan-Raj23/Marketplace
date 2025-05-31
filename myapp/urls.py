from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'myapp'
urlpatterns = [
    path('' , views.index , name='index'),
    path('product_detail/<int:product_id>/' , views.product_detail , name='product_detail'),
    path('order/<int:order_id>/' , views.after_order , name='after_order'),
    path('create_product/' , views.create_product , name='create_product'),
    path('update_product/<int:product_id>/' , views.update_product , name='update_product'),
    path('delete_product/<int:product_id>/' , views.delete_product , name='delete_product'),
    path('dashboard/' , views.dashboard ,name='dashboard'),
    path('register/' , views.register ,name='register'),
    path('login/' , auth_views.LoginView.as_view(template_name='myapp/login.html') , name='login'),
    path('logout/' , auth_views.LogoutView.as_view(template_name='myapp/logout.html') , name='logout'),
    path('invalid/' , views.invalid , name='invalid'),
    path('my_purchases/' , views.my_purchases , name='my_purchases'),
    path('sales/' , views.sales , name='sales'),
]
