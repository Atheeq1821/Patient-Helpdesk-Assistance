from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from homepage.models import Profile,Claim
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
import json
@login_required
def insurer(request):
    provider =request.user
    insurer_name = provider.username
    profiles = Profile.objects.filter(insurer=provider)
    claims=0
    members=0
    for mem in profiles:
        members+=1
        curr = mem.user
        curr_claim = Claim.objects.filter(user=curr).count()
        claims+=curr_claim
    return render(request,'insurer.html',{'insurer_name':insurer_name,'claims':claims,'members':members,'policies':'4'})

def show_users(request):
    
    return render(request,'user.html')

def show_claims(request):
    return render(request,'claims.html')


def filter_userid(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('filteruserID')
        profile = Profile.objects.get(unique_id=user_id)
        context={
            'user_id': user_id,
            'user_name':profile.name,
            'age':profile.age,
            'policy_name':profile.policy_name,
            'plan':profile.plan_type,
            'date':profile.policy_start_date,
            'claimable_amt':profile.claimable_amt,
            'claims':profile.claims,
        }
        return JsonResponse(context,safe=False)
        
def filter_policy_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        policy_name = data.get('policy_name')
        profiles = Profile.objects.filter(policy_name=policy_name)
        context=[{
            'user_id': item.unique_id,
            'user_name':item.name,
            'age':item.age,
            'policy_name':item.policy_name,
            'plan':item.plan_type,
            'date':item.policy_start_date,
            'claimable_amt':item.claimable_amt,
            'claims':item.claims,
        }for item in profiles
        ]
        return JsonResponse({'profiles':context}, safe=False)
    

def filter_userid_claims(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('filteruserID')
        profile = Profile.objects.get(unique_id=user_id)
        claimss=Claim.objects.filter(user=profile.user)
        print(profile.name)
        print(len(claimss))
        context=[]
        for c in claimss: #iterating to all claims of a single user
                context.append(
                    {
                        'claim_id': c.claim_id,
                        'user_id':profile.unique_id,
                        'name':profile.name,
                        'policy_name':profile.policy_name,
                        'applied':c.applied_date,
                        'claimed':c.claim_date,
                        'hospital':c.hospital_name,
                        'claimed_amt':c.amount_claimed,
                        'claim_info':c.treatment_info
                    }
                )

        return JsonResponse({'profiles':context}, safe=False)
        
def filter_policy_name_claims(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        policy_name = data.get('policy_name') #search key
        profiles = Profile.objects.filter(policy_name=policy_name)  #getting all profiles with searched policy
        context=[]
        for item in profiles: #iterating to all user of having searched policy
            curr_claim_user = Claim.objects.filter(user=item.user)   #getting all claims made by that user
            for c in curr_claim_user: # iterating through each claim
                context.append(
                    {
                        'claim_id': c.claim_id,
                        'user_id':item.unique_id,
                        'name':item.name,
                        'policy_name':item.policy_name,
                        'applied':c.applied_date,
                        'claimed':c.claim_date,
                        'hospital':c.hospital_name,
                        'claimed_amt':c.amount_claimed,
                        'claim_info':c.treatment_info
                    }
                )

        return JsonResponse({'profiles':context}, safe=False)