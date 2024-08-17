from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
import os
from .models import Profile,Claim
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from helpdesk.utils import Hospitals,get_balance_date,get_renew_details,get_claim_summary
from helpdesk.llm_utils import *
from django.conf import settings
import json
# Create your views here.

def custom_logout(request):
    logout(request)
    request.session['user_summary'] = ""
    print(f" logout - {request.session['user_summary']}")
    return redirect('homepage:index')




def index(request):   # Login and signup page view
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


def claim_view(curr):  #view to list all the claims made by the user
    claims = Claim.objects.filter(user=curr.user)
    return claims

def create_claim(request):
    if request.method == 'POST':
        claim_date = request.POST.get('claim_date')
        amount_claimed = request.POST.get('amount_claimed')
        treatment_info = request.POST.get('treatment_info')
        user_input = request.POST.get('user_input')
        

        claim = Claim(
            claim_date=claim_date,
            user=request.user,
            amount_claimed=amount_claimed,
            treatment_info=treatment_info
        )
        claim.save()
        claim_history=claim_view(request)
        claims_summary,claimable_amt = get_claim_summary(request,claim_history=claim_history)
        user = request.user
        profile=user.profile
        expiry = get_balance_date(start=profile.policy_start_date, dur=profile.duration)
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
        return redirect('homepage:home')
    return redirect('homepage:home')

def delete_claim(request, claim_id):
    if request.method == 'POST':
        claim = get_object_or_404(Claim, pk=claim_id)
        claim.delete()
        user=request.user
        profile=user.profile

        #making new user_summary since claim history got deleted

        claim_history=claim_view(request)
        claims_summary,claimable_amt = get_claim_summary(request,claim_history=claim_history)
        expiry = get_balance_date(start=profile.policy_start_date, dur=profile.duration)
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
    return redirect('homepage:home')  




@login_required
def home(request):
    if 'user_summary' not in request.session:  #user summary creation
        request.session['user_summary'] = ""
    user = request.user
    hospital_list=[]
    profile = user.profile
    #network hospitals ->  helpdesk/utils.py
    hospitals = Hospitals()
    hospital_list=hospitals.network_hospitals(table_name=profile.insurer,pincode=profile.pincode)


    if profile.gender=='male':  #Name to be displayed on site
        name="Mr. "+profile.name   
    else:
        name="Ms. "+profile.name


    #claim history
    claim_history=claim_view(request)
    #getting claim summary and claimable amount -> helpdesk/utils.py
    claims_summary,claimable_amt = get_claim_summary(request,claim_history=claim_history)
    
    #extracting policy summary from json file
    POLICY_JSON_PATH = os.path.join(settings.BASE_DIR, 'data','json_data','policy.json')
    with open(POLICY_JSON_PATH, 'r',encoding='utf-8') as file:
        policy_json_data = json.load(file)
    policy_details=policy_json_data[profile.policy_name] 
    summary=policy_details['summary']
    contact = policy_details['contact']


    #extracting policy features form json file
    FEATURE_JSON_PATH = os.path.join(settings.BASE_DIR, 'data','json_data','feature.json')
    with open(FEATURE_JSON_PATH, 'r',encoding='utf-8') as file:
        feature_json_data = json.load(file)
    features=[]
    for feature in policy_details['features']:
        if feature in feature_json_data:
            features.append([feature,feature_json_data[feature]])
    
    #Expiry date calculation from current date -> helpdesk/utils.py
    expiry=get_balance_date(start=profile.policy_start_date,dur=profile.duration)


    if request.session['user_summary']=="": #creating user summary -> helpdesk/llm_utils.py
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
            expiry=expiry,
            contact=contact)
        
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


def filter_hospitals(request):   # Network hospitals page view
    hospitals=Hospitals()  # Class loaded from -> helpdesk/utils.py
    if request.method=="POST":
        data = json.loads(request.body)
        filter_pin = data.get('pincode')
        user = request.user
        profile = user.profile
        h=hospitals.network_hospitals(table_name=profile.insurer,pincode=filter_pin)

        hospital_list = [
            {'name': item[0], 'city': item[1], 'address': item[2]}
            for item in h
        ]
        return JsonResponse({'hospitals': hospital_list}, safe=False)

def network_hospitals(request): #network hospitals view
    return render(request,'hospitals.html')



from django.utils.safestring import mark_safe

def renew(request):   #view for renew bonus page 
    user = request.user
    profile=user.profile
    if request.method=='POST':  #if policy renewed. New date is updated
        duration = request.POST.get('renew')
        profile.duration=int(duration)  #changing the duration as user specified
        profile.policy_start_date=timezone.now().date() # changing the policy date to current date
        profile.save()
        return redirect('homepage:home')
    
    user_details=request.session['user_summary']   #renewal bonus for user from llm model
    llm_output = get_renew_details("suraksha",user_details=user_details) # function at -> helpdesk/llm_utils.py
    safe_output = mark_safe(llm_output)
    # formatted_output = llm_output.strip()
    # renewal= formatted_output.replace('* ', '\n* ').replace('\n\n', '\n')
    return render(request,'renew.html',{'renew':safe_output})