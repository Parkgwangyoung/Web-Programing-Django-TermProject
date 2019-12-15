from django import forms
from django.forms import ModelForm
from chatting.models import Chat



class chatform(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["text","writer","writer_email","date"]
        exclude = {'writer','writer_email','date'}
        widgets = {
            'text':forms.TextInput(attrs={'size':'30','style':'height:35px; width:86%','placeholder':'글 입력'})
        }
        