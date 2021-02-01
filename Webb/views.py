from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

    
def store(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
 
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    
    return render(request, 'webb/store.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'webb/cart.html', context)

def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}

    return render(request, 'webb/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action', action)

    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
       
    else:
       customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete=True
    order.save()
    ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            postcode=data['shipping']['zipcode'],

        )
    return JsonResponse('Payment complete', safe=False)

def login_page(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user1 =authenticate(request, username=username, password=password)
        if user1 is not None:
            login(request, user1)
            return redirect('store')
        else:
            messages.info(request, 'Username or Password is Incorrect')
    
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = Customer(user=user, name=user, email=user.email)
            customer.save()
            
            messages.success(request, 'Account was created')
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def productV(request):
    # products = Product.objects.all()
    qur = request.GET.get('viewProduct')
    print(qur)
    pids = Product.objects.get(pk = qur)
    print(pids)
    context = {'pids':pids}
    return render(request, 'webb/productv.html', context)

def SearchView(request):
    
    qur = request.GET.get('search')
    prods = Product.objects.filter(name__contains = qur)
    # context=
    return render(request, 'webb/search.html', {'prods':prods})

def faq(request):
    
    context={}
    return render(request, 'webb/faq.html', context)

def sortedStore_a(request):
    products = Product.objects.all().order_by('price')
    print(products)

    data = cartData(request)
    cartItems = data['cartItems']
 
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'webb/store.html', context)

def sortedStore_d(request):
    products = Product.objects.all().order_by('price').reverse

    print (products)
    data = cartData(request)
    cartItems = data['cartItems']
 
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'webb/store.html', context)
