from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'input-class','placeholder': 'Enter your query here...','id':'user-input'}))