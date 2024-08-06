from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profile
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from helpdesk.utils import Hospitals
import json
# Create your views here.


def index(request):
    return render(request,"index.html")


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            return redirect('homepage:home')
        else:
            context = {
                'signin_error_message': 'Invalid email or password.'
            }
            return render(request, 'index.html', context)

    return redirect('homepage:index')


def signup(request):
    if request.method=='POST':
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        age=request.POST.get('age')
        password=request.POST.get('pass')
        gender=request.POST.get('options')
        phone=request.POST.get('phone')
        pincode=request.POST.get('pincode')
        insurer=request.POST.get('insurer')
        policyname=request.POST.get('policyname')
        policytype=request.POST.get('policytype')
        startdate=request.POST.get('startdate')
        duration=request.POST.get('duration')
        premium=request.POST.get('premium')
        amt=request.POST.get('amt')
        if Profile.objects.filter(user__email=email).exists():
            context = {
                'signup_error_message': 'Invalid email or password.'}
            return render(request, 'index.html', context)
        else:
            user = User.objects.create_user(username=name, email=email, password=password)
            Profile.objects.create(
                user=user,
                name=name,
                age=int(age),
                gender=gender,
                phone=phone,
                pincode=pincode,
                insurer=insurer,
                policy_name=policyname,
                plan_type=policytype,
                policy_start_date=parse_date(startdate),
                duration=int(duration),
                premium_monthly=premium,
                total_amount=amt,
            )
            login(request, user)
            return redirect('homepage:home')  
    return redirect('homepage:signup')

@login_required
def home(request):
    user = request.user
    hospital_list=[]
    profile = user.profile
    policy_name = profile.policy_name
    hospitals = Hospitals()
    hospital_list=hospitals.network_hospitals(table_name=profile.insurer,pincode=profile.pincode)
    if profile.gender=='male':
        name="Mr. "+profile.name
    else:
        name="Ms. "+profile.name
    context = {
        'name': name,
        'policyname':profile.policy_name,
        'duration':profile.duration,
        'provider':profile.insurer,
        'premium':profile.premium_monthly,
        'pincode':profile.pincode,
        'hospitals':hospital_list

    }
    return render(request,"home.html",context)


def filter_hospitals(request):
    hospitals=Hospitals()
    print("hii")
    if request.method=="POST":
        data = json.loads(request.body)
        filter_pin = data.get('pincode')
        user = request.user
        profile = user.profile
        print(filter_pin)
        h=hospitals.network_hospitals(table_name=profile.insurer,pincode=filter_pin)

        hospital_list = [
            {'name': item[0], 'city': item[1], 'address': item[2]}
            for item in h
        ]
        return JsonResponse({'hospitals': hospital_list}, safe=False)

def network_hospitals(request):
    return render(request,'hospitals.html')