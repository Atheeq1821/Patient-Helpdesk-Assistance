from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
import os
from .models import Profile,Claim
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from helpdesk.utils import Hospitals,get_balance_date,get_renew_details
from helpdesk.llm_utils import *
from django.conf import settings
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


def claim_view(curr):
    claims = Claim.objects.filter(user=curr.user)
    return claims

def create_claim(request):
    if request.method == 'POST':
        claim_date = request.POST.get('claim_date')
        amount_claimed = request.POST.get('amount_claimed')
        treatment_info = request.POST.get('treatment_info')
        user_input = request.POST.get('user_input')
        
        # Create and save the claim
        claim = Claim(
            claim_date=claim_date,
            user=request.user,
            amount_claimed=amount_claimed,
            treatment_info=treatment_info
        )
        claim.save()
        return redirect('homepage:home')
    return redirect('homepage:home')

@login_required
def home(request):
    if 'user_summary' not in request.session:
        request.session['user_summary'] = ""
    user = request.user
    hospital_list=[]
    profile = user.profile


    #network hospitals
    hospitals = Hospitals()
    hospital_list=hospitals.network_hospitals(table_name=profile.insurer,pincode=profile.pincode)
    if profile.gender=='male':
        name="Mr. "+profile.name
    else:
        name="Ms. "+profile.name


    #claim history
    claim_history=claim_view(request)
    claimable_amt = profile.total_amount
    claims_summary=""
    claim_count=0
    for claims in claim_history:
        claim_count+=1
        claimable_amt-=claims.amount_claimed
        claims_summary+=f" Claim ID ->{claims.claim_id} , Claim-date->{claims.claim_date}, Claim-amt ->{claims.amount_claimed} , Treatment Info -> {claims.treatment_info} \n"
    
    claims_summary=f"Number of claims made by the user is {claim_count} \n"+claims_summary
    print(claims_summary)

    #features
    POLICY_JSON_PATH = os.path.join(settings.BASE_DIR, 'data','json_data','policy.json')
    with open(POLICY_JSON_PATH, 'r',encoding='utf-8') as file:
        policy_json_data = json.load(file)
    policy_details=policy_json_data[profile.policy_name] 
    summary=policy_details['summary']


    FEATURE_JSON_PATH = os.path.join(settings.BASE_DIR, 'data','json_data','feature.json')
    with open(FEATURE_JSON_PATH, 'r',encoding='utf-8') as file:
        feature_json_data = json.load(file)
    features=[]
    for feature in policy_details['features']:
        if feature in feature_json_data:
            features.append([feature,feature_json_data[feature]])
            
    #date calculation
    expiry=get_balance_date(start=profile.policy_start_date,dur=profile.duration)

    request.session['user_summary'] = get_user_summary(
        name=profile.name,
        age=profile.age,
        policy=profile.policy_name,
        type=profile.plan_type,
        gender=profile.gender,
        claims=claims_summary,
        policy_start_date=profile.policy_start_date,
        premium=profile.premium_monthly,
        amt=profile.total_amount,
        expiry=expiry)
    context = {
        'name': name,
        'policyname':profile.policy_name,
        'duration':expiry,
        'provider':profile.insurer,
        'premium':profile.premium_monthly,
        'pincode':profile.pincode,
        'hospitals':hospital_list,
        'claims':claim_history,
        'claimable_amt':claimable_amt,
        'summary':summary,
        'features':features,
        'policy_link': policy_details['link']

    }
    return render(request,"home.html",context)

# def get_policy_details(policy_name):
#     return data.get(policy_name, "Policy not found")
def filter_hospitals(request):
    hospitals=Hospitals()
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




def renew(request):
    print("renew")
    user = request.user
    profile=user.profile
    if request.method=='POST':
        print("hii")
        duration = request.POST.get('renew')
        profile.duration=int(duration)
        # return render(request,'renew.html')
        profile.policy_start_date=timezone.now().date()
        profile.save()
        return redirect('homepage:home')
    user_details=request.session['user_summary']
    llm_output = get_renew_details("suraksha",user_details=user_details)
    # formatted_output = llm_output.strip()
    # renewal= formatted_output.replace('* ', '\n* ').replace('\n\n', '\n')
    return render(request,'renew.html',{'renew':llm_output})