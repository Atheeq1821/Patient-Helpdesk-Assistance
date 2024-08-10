from django.shortcuts import render
from django.http import JsonResponse
from .forms import ChatForm
from .pipeline.llmpipelines import activate_qroq
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def assistant(request):
    if 'conversation_history' not in request.session:
        request.session['conversation_history'] = []
    if request.method == 'POST':
        form = ChatForm(request.POST)
        print("form loadede")
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            print(user_input)
            conversation_history = request.session['conversation_history']
            model_output=activate_qroq(user_query=user_input,policy_name="suraksha",conversation_history=conversation_history)
            
            conversation_history.append({
                'user': user_input,
                'model': model_output
            })
            print(conversation_history)
            request.session['conversation_history'] = conversation_history
            response_data = {
                'user': "You: " + user_input,
                'model': "Bot: " + model_output 
            }
            return JsonResponse(response_data)
    else:
        form = ChatForm()
        return render(request, 'chat.html', {'form': form})

