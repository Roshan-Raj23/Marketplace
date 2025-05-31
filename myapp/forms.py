from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import OrderDetail , Product

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['quantity']
        
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'id': 'numberInput',
                'class': 'w-20 outline-none border-2 border-gray-300 rounded-md px-2 py-1 focus:border-blue-300',
                'type': 'number',
                'min': 1,
                'value': 1,
                'onInput': 'resizeInput()'
            }),
        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name' , 'description' , 'price' , 'file']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'outline-none border-2 border-gray-300 rounded-md px-2 py-1 focus:border-blue-300',
            }),
            'description': forms.TextInput(attrs={
                'class': 'outline-none border-2 border-gray-300 rounded-md px-2 py-1 focus:border-blue-300',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'outline-none border-2 border-gray-300 rounded-md px-2 py-1 focus:border-blue-300',
            }),
            'file': forms.FileInput(attrs={
                'class': 'outline-none border-2 border-gray-300 rounded-md px-2 py-1 focus:border-blue-300',
            }),
        }
        
class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')
        