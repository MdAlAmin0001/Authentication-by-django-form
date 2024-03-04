from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

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






