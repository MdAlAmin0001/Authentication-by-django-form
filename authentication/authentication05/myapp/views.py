from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

from authentication01.settings import EMAIL_HOST_USER
import random
from django.core.mail import send_mail

def signup(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginpage')
    else:
        form=SignUpForm()
    return render(request, 'signup.html', {'form':form})

def loginpage(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form=login_form()
    return render(request, 'loginpage.html',{'form':form})


def logoutpage(request):
    logout(request)
    return redirect('loginpage')

def home(request):
    return render(request, 'home.html')

def profile(request):
    user_profile = get_object_or_404(Custom_user, pk=request.user.pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})


def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Custom_user.objects.get(email=email)
            otp = random.randint(111111, 999999)
            user.otp_token = otp
            user.save()

            
            subject = f"Important: Your One-Time Password {otp}"

            msg = f"""
            Dear {user.display_name} ,

            We received a request to verify your identity.
            Your one-time password is: {otp}

            Please enter this code to complete your request.

            For your security:

            * Never share your OTP with anyone.
            * This code is valid only for [2 minutes].
            * Delete this email once you've used the OTP.

            If you didn't request this OTP, please contact us immediately

            Sincerely,

            The Developer Team
            """
            from_mail = EMAIL_HOST_USER
            recipient = [email]
            send_mail(
                subject=subject,
                recipient_list=recipient,
                from_email=from_mail,
                message=msg,
            )
            return render(request, 'changepassword.html', {'email': email})
        except Custom_user.DoesNotExist:
            # Email not found in the database
            message = "Email address not found. Please check and try again."
            return render(request, 'forgetpassword.html', {'error_message': message})
    else:
        return render(request, 'forgetpassword.html')


def changepassword(request):
    if request.method == "POST":
        mail = request.POST.get('email')
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        user = Custom_user.objects.get(email = mail)
        if user.otp_token != otp:
            return redirect('forgetpassword')
        if password != c_password:
            return redirect('forgetpassword')
        user.set_password(password)
        
        user.save()
        return redirect('loginpage')
    return render(request, 'changepassword.html')


# update funtion by new models like model name, product title, description
# def search_query(request):
#     if request.method == 'POST':
#         query=request.POST.get('search')
#         search_post=post_product.objects.filter(
#             Q(Product_Title__icontains=query) | Q(Product_Description__icontains=query)
#         )
#     return render(request, 'Shop.html',{'sq':search_post})

#set it on template
# {% for i in sq %}
# <div class="product-card">
#     <img src="/{{i.Product_Image}}" alt="Product Photo" class="img-fluid mb-3">
#     <h4>{{i.Product_Title}} - {{i.quantity}} kg</h4>
#     <h5>Price: {{i.Product_price}} Taka</h5>






