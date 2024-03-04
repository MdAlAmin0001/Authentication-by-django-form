from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

from django.contrib.auth import get_user_model
from myapp.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.core.mail import EmailMessage
from authentication01.settings import EMAIL_HOST_USER
import random
from django.core.mail import send_mail

def activate(request,uid64,token):
    User=get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(pk=uid)

    except:
        user =None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('loginpage')

    print("account activation: ", account_activation_token.check_token(user, token))

    return redirect('loginpage')


def activateEmail(request,user,to_mail):
    mail_sub='Active your user Account'
    message=render_to_string("template_activate.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })
    email= EmailMessage(mail_sub, message, to=[to_mail])
    if email.send():
        messages.success(request,f'Dear')
    else:
        message.error(request,f'not')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('loginpage')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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


@login_required
def logoutpage(request):
    logout(request)
    return redirect('loginpage')


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
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


# # update funtion by new models like model name, product title, description
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