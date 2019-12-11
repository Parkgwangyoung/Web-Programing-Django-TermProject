from django import forms
from django.forms import ModelForm
from mail.models import Mail



class CreateMailform(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ["attn_email","title","description","date","writer","writer_email"]
        exclude = {'date','writer','writer_email'}
        widgets = {
            'title':forms.TextInput(attrs={'size':'30','style':'height:35px;','placeholder':'제목을 입력하세요.'}),
            'description' : forms.Textarea(attrs={'size':'100','style':'height:100;width:100%'}),
            'attn_email':forms.TextInput(attrs={'size':'30','style':'height:35px;','placeholder':'받는 사람 이메일주소'}),

        }
        labels = {"title":"제 목","description":"내 용","attn_email":"받는사람 메일주소"}


    def __init__(self,*args,**kwargs):
        super(CreateMailform,self).__init__(*args,**kwargs)
        self.label_suffix=''
