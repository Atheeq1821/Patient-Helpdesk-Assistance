from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profile
from django.utils.dateparse import parse_date
# Create your views here.
def home(request):
    return render(request,"index.html")


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        # Authenticate the user using email
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            # If authentication is successful, log the user in
            print("success")
            login(request, user)
            messages.error(request, 'success.')
            return redirect('home')  # Redirect to the home page or another page
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid email or password')
            return redirect('signin')  # Redirect back to the sign-in page

    return redirect('home')


def signup(request):
    if request.method=='POST':
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        age=request.POST.get('age')
        password=request.POST.get('pass')
        gender=request.POST.get('options')
        phone=request.POST.get('phone')
        pincode=request.POST.get('pincode')
        policyname=request.POST.get('policyname')
        policytype=request.POST.get('policytype')
        startdate=request.POST.get('startdate')
        duration=request.POST.get('duration')
        premium=request.POST.get('premium')
        amt=request.POST.get('amt')
        if Profile.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('home')
        else:
            user = User.objects.create_user(username=name, email=email, password=password)
            Profile.objects.create(
                user=user,
                name=name,
                age=int(age),
                gender=gender,
                phone=phone,
                pincode=pincode,
                policy_name=policyname,
                plan_type=policytype,
                policy_start_date=parse_date(startdate),
                duration=int(duration),
                premium_monthly=premium,
                total_amount=amt,
            )
            login(request, user,backend='your_app_name.backends.EmailBackend')
            return redirect('home')  
    return redirect('home')
