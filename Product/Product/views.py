from multiprocessing import context
from django.shortcuts import render,redirect
from .models import Product, ProductForm
# Create your views here.
def index(request):

    return render(request,'index.html');

def addProduct(request):
    if request.method=='POST':
        p=Product();
        p.name=request.POST['pname'];
        p.brand=request.POST['pbrand'];
        p.description=request.POST['pdescription'];
        p.category=request.POST['pcategory'];
        p.price=request.POST['pprice'];
        p.quantity=request.POST['pquantity'];
        p.colors=request.POST.getlist('colors');
        p.image=request.FILES['pimage'];
        p.save();
        return redirect('/');
    else:
        return render(request,'addProduct.html')
def add(request):
    context={}
    form=ProductForm(request.POST or None)
    if form.is_valid():
        form.save();
    context['form']=form;
    return render(request,'add.html');

