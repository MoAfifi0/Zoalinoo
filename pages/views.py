from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from products.models import Product
from .models import Contact

# Create your views here.

def index(request):
    context = {
        'products': Product.objects.all()
    }
    return render( request , 'pages/index.html' , context )

def about(request):
    return render( request , 'pages/about.html' )

def contact(request):
    if request.method=="POST":
        contact=Contact()
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        contact.fname=fname
        contact.lname=lname
        contact.email=email
        contact.subject=subject
        contact.save()
        messages.success(request, 'Thanks For Contact Us')
    return render(request, "pages/contact.html")

def zoalinoo(request):
    return render( request , 'pages/zoalinoo.html' )