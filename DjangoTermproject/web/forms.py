from django import forms
from django.forms import ModelForm
from web.models import BoardTable,Board


class CreatePostform(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["board_type","title","description","date","writer"]
        exclude =['board_type','date','writer',]
        widgets = {
            'title':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
            'description' : forms.Textarea(attrs={'size':'100','style':'height:100;'}),

        }
        labels = {"title":"제 목","description":"내 용"}

    def __init__(self,*args,**kwargs):
        super(CreatePostform,self).__init__(*args,**kwargs)
        self.label_suffix=''



class BtCreateform(forms.ModelForm):
    class Meta:
        model = BoardTable
        fields = ["board_name"]
        widgets = {'board_name':forms.TextInput(attrs={'size':'30','style':'height:30;'})}
        labels = {"board_name":"만들고 싶은 게시판 명 "}

    def __init__(self,*args,**kwargs):
        super(BtCreateform,self).__init__(*args,**kwargs)
        self.label_suffix=''

class Bcreateform(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["board_type","title","description","writer","date"]
        exclude = ['date',]
        widgets = {
            'title':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
            'description':forms.Textarea(attrs={'size':'100','style':'height:100;'}),
            'writer':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
        }
        labels = {"board_type":"만들 게시판 명","title":"제 목","description":"글 내용","writer":"작 성 자"}

    def __init__(self,*args,**kwargs):
        super(Bcreateform,self).__init__(*args,**kwargs)
        self.label_suffix=''