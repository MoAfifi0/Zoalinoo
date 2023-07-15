from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from products.models import Product
import re

# Create your views here.

def signin(request):
    if request.method == 'POST' and 'btnsignin' in request.POST:

        username = request.POST['user']
        password = request.POST["pass"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            #messages.success(request, 'You are loggin in')
        else:
            messages.error(request, 'Username or password invalid')

        return redirect('signin')
    else:
        return render( request , 'accounts/signin.html' )

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:

        #variables for fields
        fname = None
        lname = None
        address = None
        address2 = None
        city = None
        state = None
        zip_number = None
        email = None
        username = None
        password = None
        terms = None
        is_added = None

        #Get values from the form
        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in First Name')

        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in Last Name')

        if 'address' in request.POST: address = request.POST['address']
        else: messages.error(request, 'Error in Address')

        if 'address2' in request.POST: address2 = request.POST['address2']
        else: messages.error(request, 'Error in Address 2')

        if 'city' in request.POST: city = request.POST['city']
        else: messages.error(request, 'Error in City')

        if 'state' in request.POST: state = request.POST['state']
        else: messages.error(request, 'Error in State')

        if 'zip' in request.POST: zip_number = request.POST['zip']
        else: messages.error(request, 'Error in Zip')

        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request, 'Error in Email')

        if 'user' in request.POST: username = request.POST['user']
        else: messages.error(request, 'Error in Username')

        if 'pass' in request.POST: password = request.POST['pass']
        else: messages.error(request, 'Error in Password')

        if 'terms' in request.POST: terms = request.POST['terms']

        #Check the Values
        if fname and lname and address and address2 and city and state and zip_number and email and username and password:
            if terms == 'on':
                #Check if username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This username is taken')
                else:
                    #Check if email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is taken')
                    else:
                        patt = "^\w+([.']\w+)*@\w+([-.])*\.\w+([-.]\w+)*$"
                        if re.match(patt, email):
                            #add user
                            user = User.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password=password)
                            user.save()
                            #add user profile
                            userprofile = UserProfile(user=user, address=address, address2=address2, city=city, state=state, zip_number=zip_number)
                            userprofile.save()
                            #Clear Fields
                            fname = ''
                            lname = ''
                            address = ''
                            address2 = ''
                            city = ''
                            state = ''
                            zip_number = ''
                            email = ''
                            username = ''
                            password = ''
                            terms = None
                            #Success Message
                            messages.success(request, 'Your account is created')
                            is_added = True
                        else:
                           messages.error(request, 'Invalid Email') 
            else:
                messages.error(request, 'You must agree to the terms')
        else:
            messages.error(request, 'Check empty fields')
        
        return render(request, 'accounts/signup.html',{
            "fname":fname,
            "lname":lname,
            "address":address,
            "address2":address2,
            "city":city,
            "state":state,
            "zip_number":zip_number,
            "email":email,
            "username":username,
            "password":password,
            "is_added":is_added
        })
    else:
        return render(request, 'accounts/signup.html')

def profile(request):
    if request.method == 'POST' and 'btnsave' in request.POST:

        if request.user is not None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)

            if request.POST['fname'] and request.POST['lname'] and  request.POST['address'] and request.POST['address2'] and request.POST['city'] and request.POST['state'] and request.POST['zip'] and request.POST['email'] and request.POST['user'] and request.POST['pass']:
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                userprofile.address = request.POST['address']
                userprofile.address2 = request.POST['address2']
                userprofile.city = request.POST['city']
                userprofile.state = request.POST['state']
                userprofile.zip_number = request.POST['zip']
                #request.user.email = request.POST['email']
                #request.user.username = request.POST['user']
                if not request.POST['pass'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['pass'])
                request.user.save()
                userprofile.save()
                auth.login(request, request.user)
                messages.success(request, 'Your data has been saved')
            else:
                messages.error(request, 'Check your values and elements')

        return redirect('profile')
    else:
        if request.user is not None:

            context = None

            if not request.user.is_anonymous:

                userprofile = UserProfile.objects.get(user=request.user)

                context = {
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'state':userprofile.state,
                    'zip_number':userprofile.zip_number,
                    'email':request.user.email,
                    'user':request.user.username,
                    'pass':request.user.password
            }
            return render( request , 'accounts/profile.html', context)
        else:
            return render('profile')
        

def product_favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user, product_favorites=pro_fav).exists():
            messages.success(request, 'Already product in the favorite list')
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request, 'Product has been favorited')
    else:
        messages.error(request, 'You must be logged in')

    return redirect('/products/' + str(pro_id))

def show_product_favorite(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        context = { 'products':pro }
    return render(request, 'products/products.html', context)