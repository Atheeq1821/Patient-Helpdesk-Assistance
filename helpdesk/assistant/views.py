from django.shortcuts import render
from django.http import JsonResponse
from .forms import ChatForm
from .pipeline.llmpipelines import generate_pre_output
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def assistant(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        print("form loadede")
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            print("valid form")
            model_output=generate_pre_output(user_input,"suraksha")
            # conversation_history_list = [{"user": "hii", "model": "byee"}]
            response_data = {
                'user': "You: " + user_input,
                'model': "Bot: " + model_output 
            }
            return JsonResponse(response_data)
    else:
        form = ChatForm()
        return render(request, 'chat.html', {'form': form})

