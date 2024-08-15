from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
import random
import os
from datetime import datetime, timedelta
from decimal import Decimal
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

def delete_all_users():
    users_with_profiles = User.objects.filter(profile__isnull=False)
    users_with_profiles.delete()
    print("All users with profiles have been deleted.")


from dateutil.relativedelta import relativedelta
def generate_claims():
    profiles = Profile.objects.all()
    treatment_info_samples = [
        "Heart surgery", "Kidney transplant", "Cancer treatment", 
        "Fracture repair", "Diabetes management", "Orthopedic surgery", 
        "Neurology treatment", "Liver transplant", "Gastric bypass surgery", "ENT treatment"
        ]
    min_days_before_policy_expiry = 70
    for profile in profiles:
        pin = profile.pincode
        insurer = profile.insurer
        hospitals =Hospitals()
        hospital_list = hospitals.network_hospitals(table_name=insurer, pincode=pin)
        hospital_names =[item[0] for item in hospital_list]
        hospital_names.append('Pavitra hospital')

        num_claims = random.randint(2, 10)
        policy_expiry = profile.policy_start_date + relativedelta(years=profile.duration)


        for j in range(num_claims):
            if profile.claimable_amt>=5000:
                claimable_amt_float = float(profile.claimable_amt)
                claim_amount = Decimal(abs(round(random.uniform(5000, claimable_amt_float), 2)))
                potential_applied_date = policy_expiry - timezone.timedelta(days=min_days_before_policy_expiry)
                applied_date = min(potential_applied_date, timezone.now().date())
                claim_date = applied_date + timezone.timedelta(days=random.randint(2, 3)) 
                claim = Claim(
                user=profile.user,
                applied_date=applied_date,
                claim_date = claim_date,
                hospital_name=random.choice(hospital_names),
                amount_claimed=claim_amount,
                treatment_info=random.choice(treatment_info_samples)
                )
                claim.save()
                print(f"{j} of {profile.user}")
    print("Multiple claims have been created for all profiles, with applied dates 70 days before the policy expiry.")


def generate_users():
    insurer_policies = {
    'hdfc': ['energy', 'suraksha', 'medisure', 'optimasecure'],
    'care': ['care', 'caresupreme', 'caresenior', 'careyouthplus', 'careheart', 'careclassic'],
    'nivabupa': ['goactive', 'heartbeat', 'healthpulse', 'seniorfirstgold'],
    'bajajallianz': ['healthguardsilver', 'healthensurefamily', 'healthcaresupreme', 'healthguardplatinum']
    }
    plan_types = ['individual', 'gold', 'silver', 'family', 'platinum']
    pincodes = ['600001', '600020', '600017', '600112', '600025', '600032', '600040', '600008', '600118', '600110']
    names = [
    "Arjun", "Siva", "Ravi", "Lakshmi", "Nandini", "Kumar", "Anjali", "Rajesh", "Meera", "Vijay",
    "Prakash", "Sneha", "Ajay", "Geetha", "Ramesh", "Madhavi", "Deepak", "Sonia", "Amit", "Neha",
    "Vikram", "Pooja", "Anand", "Swathi", "Manoj", "Kavita", "Sunil", "Dhileep", "Meena", "Sandeep",
    "Nisha", "Kiran", "Venu", "Jaya", "Lalitha", "Suresh", "Divya", "Banu", "Rajini", "Krishna",
    "Rupa", "Harish", "Archana", "Anil", "Rajalakshmi", "Srinivasan", "Latha", "Karthik", "Naveen", "Rani",
    "Suman", "Shivani", "Siddharth", "Bhavna", "Raj", "Aruna", "Gaurav", "Asha", "Sanjay", "Rekha",
    "Gita", "Siddhi", "Ajit", "Jayanthi", "Nikhil", "Anita", "Krishnan", "Neelam", "Sumanth", "Shweta",
    "Nitin", "Sunita", "Rajeshwari", "Manju", "Shankar", "Sita", "Sushila", "Deepa", "Maya", "Arun",
    "Sridhar", "Jyothi", "Rajendra", "Pallavi", "Kavitha", "Sushma", "Ravi Kumar", "Rohit", "Madhuri", "Aarti",
    "Rajesh", "Amitabh", "Vandana", "Ganga", "Sangeeta", "Haritha", "Bhargav", "Chitra", "Vinod", "Sushil"
    ]
    genders = [
    "Male", "Male", "Male", "Female", "Female", "Male", "Female", "Male", "Female", "Male",
    "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
    "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
    "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
    "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
    "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
    "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
    "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
    "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female"
    ]
    ages = [
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
    35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
    45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
    55, 56, 57, 58, 59, 60, 61, 62, 63, 64,
    65, 66, 67, 68, 69, 70, 25, 26, 27, 28,
    29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
    39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
    49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
    59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
    69, 70
    ]
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now()
    for i in range(6,100):
        username = names[i]
        e_n=username.lower()
        email = f"{e_n}@gmail.com"
        password = "12345"
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Randomly select insurer and corresponding policy
        insurer = random.choice(list(insurer_policies.keys()))
        policy_name = random.choice(insurer_policies[insurer])

        # Randomly select plan type (with 'individual' more frequently)
        plan_type = 'individual' if random.random() > 0.5 else random.choice(plan_types)

        # Randomly select a pincode from Tamil Nadu
        pincode = random.choice(pincodes)
        amt=round(random.uniform(100000, 10000000), 2)
        # Create Profile
        profile = Profile(
            user=user,
            name=username,
            age=ages[i],
            gender=genders[i],
            phone=f"98765{random.randint(10000, 99999)}",
            pincode=pincode,
            insurer=insurer,
            policy_name=policy_name,
            plan_type=plan_type,
            policy_start_date=generate_random_date(start_date, end_date).date(),
            duration=random.randint(1, 20),  # duration in years
            premium_monthly=round(random.uniform(1000, 10000), 2),
            total_amount=amt,
            claimable_amt=amt,
            claims=0
        )
        profile.save()
        print(i)

    print("10 users and their profiles have been created.")

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)
def index(request):   # Login and signup page view
    # generate_users()
    # delete_all_users()
    # generate_claims()
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

def insurer_login(request):
    if request.method=='POST':
        insurer=request.POST.get('cc-id')
        email=request.POST.get('cc-email')
        password=request.POST.get('cc-pass')
        try:
            user = authenticate(request, username=insurer, password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            return redirect('insurer:insurer')
        else:
            context = {
                'login_error_message': 'Invalid email or password.'
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
        print(f"Summary from create claim {request.session['user_summary']}")
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
        print(f"Sumamry form delete  : {request.session['user_summary']}")
    return redirect('homepage:home')  




@login_required
def home(request):
    if 'user_summary' not in request.session:  #user summary creation
        print("inside session creation")
        request.session['user_summary'] = ""
    user = request.user
    hospital_list=[]
    profile = user.profile

    print(f" Inside main - {request.session['user_summary']}")
    #network hospitals ->  helpdesk/utils.py
    hospitals = Hospitals()
    hospital_list=hospitals.network_hospitals(table_name=profile.insurer,pincode=profile.pincode)


    if profile.gender=='male' or profile.gender=='Male':  #Name to be displayed on site
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
    # print(f"Summary form home {request.session['user_summary']}")
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

