from ast import NotEq
from lib2to3.pgen2.token import EQUAL
import re
from unicodedata import category
from xmlrpc.client import DateTime
from django.shortcuts import render,redirect
from .models import Cart, DeatiledOrder, Order, Registration
from django.contrib import messages
import qrcode
import cv2
import urllib.request
from django.db.models import Q
from PIL import Image
from django.contrib.postgres.fields import ArrayField
from multiprocessing import context
from .models import Product
from datetime import date, datetime
# , ProductForm

# Create your views here.
# def home(request):
#     return render(request, 'registration.html')

def register(request):
    context = {}
    context['category'] = "Buyer"
    if(request.method == "POST"):
        # print("reg1")
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        address = request.POST['address']
        mobileNo = request.POST['mobileno']
        category = request.POST['category']

        if password1 == password2:
            if(Registration.objects.filter(name = username).exists()):
                # print('User name is not available')
                # print("reg2")
                messages.info(request, 'User name is not available')
                return redirect('register')
            elif(Registration.objects.filter(email = email).exists()):
                # print('Email id is already taken')
                messages.info(request, 'Email id is already taken')
                return redirect('register')
            else:
                # print("reg3")
                user = Registration()
                user.name = username
                user.password = password1
                user.email = email
                user.address = address
                user.mobileNo = mobileNo
                user.category = category
                user.save()
                
                # save_name = username + ".png"
                # urllib.request.urlretrieve(img)
                # print('User Created')
        else:
            # print("Terminal Message: Password not matching.")
            messages.info(request, 'Password not matching.')
            return redirect('register')
        return redirect("/login/")
    else:
        return render(request, 'registration.html',context)

def displayAllCustomer(request):
    context = {}
    context['category'] = 'Admin'
    listOfCustomers=list(Registration.objects.all())
    customer=Registration.objects.get(id = request.session['id'])
    listOfCustomers.remove(customer)
    context['listOfCustomers']=listOfCustomers
    return render(request,'displayAllCustomer.html',context)
    
def addProduct(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    if request.method=='POST':
        p=Product()
        p.name=request.POST['pname']
        p.brand=request.POST['pbrand']
        p.description=request.POST['pdescription']
        p.category=request.POST['pcategory']
        p.price=request.POST['pprice']
        p.quantity=request.POST['pquantity']
        p.colors=request.POST.getlist('colors')
        p.image=request.FILES['pimage']
        data = Registration.objects.get(id = request.session['id'])
        p.customer = data
        p.save()
        return redirect('displayProduct')
    else:
        return render(request,'addProduct.html',context)

def login(request):
    # print('in login')
    context = {}
    context['category'] = "Buyer"
    if(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        if(Registration.objects.filter(name = username).exists() and Registration.objects.filter(password = password).exists()):
            request.session['id'] = (Registration.objects.get(name=username)).id
            request.session['name'] = (Registration.objects.get(name=username)).name
            category = (Registration.objects.get(name=username)).category
            
            context['category'] = category
            print(request.session['id'])
            print(request.session['name'])
            # print('User is logged in')
            return render(request,'index.html',context)
        else:
            messages.info(request, 'Username or Password not matching.')
            return render(request,'login.html',context)
    else:
        return render(request,'login.html',context)

def logout(request):
    request.session.pop('id')
    return redirect('/login/')

def contact_us(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    return render(request,'contact_us.html',context)

def index(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    listOfProducts = list(Product.objects.all())
    
    context['listOfProducts'] = listOfProducts
    return render(request,'index.html',context)

def indexCategory(request,category1):
    context={}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    listOfProducts=Product.objects.filter(category=category1)
    context['listOfProducts']=listOfProducts
    return render(request,'index.html',context)

def product_details(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    return render(request,'product_details.html',context)

def updateProduct(request,id):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    if(request.method=="POST"):
        p=Product.objects.get(id = id);
        p.name=request.POST['pname'];
        p.brand=request.POST['pbrand'];
        p.description=request.POST['pdescription'];
        p.category=request.POST['pcategory'];
        p.price=request.POST['pprice'];
        p.quantity=request.POST['pquantity'];
        p.colors=request.POST.getlist('colors');
        p.image=request.FILES['pimage'];
        data=Registration.objects.get(id=request.session['id']);
        p.customer=data;
        p.save()
        return redirect('/displayProduct/');
    else:
        p = Product.objects.get(id = id);
        context['product']=p
        return render(request,'updateProduct.html',context)

def displayProduct(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    listOfProducts = list(Product.objects.filter(customer_id = request.session['id']))
    context['listOfProducts'] = listOfProducts
    return render(request, 'displayProduct.html', context)
    # return render(request, 'index.html')

def updateProfile(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    if(request.method == "POST"):
        
        cusId= (Registration.objects.get(id=request.session['id'])).id
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        address = request.POST['address']
        mobileNo = request.POST['mobileno']

        listOfCustomers = list(Registration.objects.filter(name = username))
        for customer in listOfCustomers:
            if(customer.id != cusId):
                messages.info(request, 'User name is already taken')
                return redirect('/updateProfile/')

        listOfCustomers = list(Registration.objects.filter(email = email))
        for customer in listOfCustomers:
            if(customer.id != cusId):
                messages.info(request, 'Email id is already taken')
                return redirect('/updateProfile/')
        else:
                c=Registration.objects.get(id=request.session['id'])
                c.name=username
                c.password=password
                c.email=email
                c.address=address
                c.mobileNo=mobileNo
                # img.save('media/user/'+username + ".png")
                c.save()
                return redirect("/displayProfile/")
    else:
        c=Registration.objects.get(id = request.session['id'])
        context['customer']=c
        return render(request,'updateProfile.html',context)

def displayProfile(request):
    context={}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    context['customer']=Registration.objects.get(id=request.session['id'])
    return render(request,'displayProfile.html',context)

def deleteProfile(request):
    customer=Registration.objects.get(id=request.session['id'])
    customer.delete()
    messages.info(request, "You logged out from the system because you have deleted your profile")
    return redirect('/register/')

def deleteProduct(request,id):
    product = Product.objects.filter(id = id)
    product.delete()
    return redirect('/displayProduct/')


# Cart

def addToCart(request,id):
        c = Cart()
        c.productId = id
        c.productName = (Product.objects.get(id = id)).name
        c.customerId = request.session['id']
        c.image = (Product.objects.get(id = id)).image
        c.price = (Product.objects.get(id = id)).price
        c.quantity = 1
        if(Cart.objects.filter(productId=id,customerId=c.customerId).exists()):
            return redirect('cart')
        else:
            c.save()
        return redirect('index')
     
def cart(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    listOfProducts = list(Cart.objects.filter(customerId = request.session['id']))
    context['listOfProducts'] = listOfProducts 
    totalPrice = 0
    for cartItem in listOfProducts:
        totalPrice += cartItem.price * cartItem.quantity
    context['totalPrice'] = totalPrice
    return render(request,'cart.html', context)

def deleteCartItem(request,id):
    cartItem = Cart.objects.get(productId=id, customerId= request.session['id'])
    cartItem.delete()
    return redirect('cart')

def checkout(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    listOfProducts = list(Cart.objects.filter(customerId = request.session['id']))
    context['listOfProducts'] = listOfProducts 
    totalPrice = 0
    for cartItem in listOfProducts:
        totalPrice += cartItem.price * cartItem.quantity
    context['totalPrice'] = totalPrice
    context['address'] = (Registration.objects.get(id = request.session['id'])).address
    return render(request,'checkout.html',context)

def updateAddress(request):
    customer = Registration.objects.get(id = request.session['id'])
    customer.address = request.POST['address']
    customer.save()
    return redirect('checkout')

def increaseQuantity(request,id):
    c=Cart.objects.get(productId=id, customerId= request.session['id'])
    if Product.objects.get(id=id).quantity >= c.quantity+1:
        c.quantity = c.quantity+1
        c.save()
    else:
        messages.info(request, 'This product is now not in stock')
    return redirect('cart')

def decreaseQuantity(request,id):
    c=Cart.objects.get(productId=id, customerId= request.session['id'])
    if c.quantity == 1:
        return redirect('cart')
    c.quantity = c.quantity-1
    c.save()
    return redirect('cart')

def addOrder(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    address = request.POST['address']
    method = request.POST['method']
    order = Order()
    order.customerId = request.session['id']
    order.address = address
    order.method = method
    order.date = datetime.today()
    order.save()
    id = order.id

    listOfProducts = list(Cart.objects.filter(customerId = request.session['id']))
    for cartItem in listOfProducts:
        detailedOrder = DeatiledOrder()
        detailedOrder.orderId = id
        detailedOrder.customerId = request.session['id']
        detailedOrder.productId = cartItem.productId
        detailedOrder.productName = cartItem.productName
        product=Product.objects.get(id=detailedOrder.productId)
        product.quantity=product.quantity-cartItem.quantity
        if(product.quantity == 0):
            product.delete()
        else:
            product.save() 
        detailedOrder.quantity = cartItem.quantity
        detailedOrder.price = cartItem.price
        detailedOrder.save()
        cartItem.delete()

    context['listOfProducts'] = listOfProducts
    context['order'] = order
    totalPrice = 0
    for cartItem in listOfProducts:
        totalPrice += cartItem.price * cartItem.quantity
    context['totalPrice'] = totalPrice
    return render(request, 'generateBill.html',context)

def orderHistory(request):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    listOfOrders = list(Order.objects.filter(customerId = request.session['id']))
    context['listOfOrders'] = listOfOrders
    return render(request, 'orderHistory.html', context)

def displayOrder(request,id):
    context = {}
    category = (Registration.objects.get(id = request.session['id'])).category
    context['category'] = category
    listOfOrders=list(DeatiledOrder.objects.filter(orderId=id))
    context['listOfOrders']=listOfOrders
    totalPrice = 0
    for item in listOfOrders:
        totalPrice += item.price * item.quantity
    context['totalPrice'] = totalPrice
    return render(request,'displayOrder.html',context)


# def add(request):
#     context={}
#     form=ProductForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#     context['form']=form
#     return render(request,'add.html')