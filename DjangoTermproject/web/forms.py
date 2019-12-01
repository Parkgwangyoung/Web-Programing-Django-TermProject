from django import forms
from django.forms import ModelForm
from web.models import BoardTable,Board,Post

class CreatePostform(forms.ModelForm):
    class Meta:
        model = Post
        fileds = ["board_name","title","description","date","writer"]
        exclude = ['board_name','date','writer',]
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
        fields = ["board_type",]
        widgets = {'board_type':forms.TextInput(attrs={'size':'11','style':'height:30;','placeholder':'여기에 입력'})}
        labels = {"board_type":"상위 게시판 이름"}

    def __init__(self,*args,**kwargs):
        super(BtCreateform,self).__init__(*args,**kwargs)
        self.label_suffix=''

class Bcreateform(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["board_type","board_name"]
        widgets = {'board_name':forms.TextInput(attrs={'size':'20','style':'height:30;','placeholder':'여기에 입력'})}
        labels = {"board_name":"하위 게시판 이름","board_type":"상위 게시판 이름"}

    def __init__(self,*args,**kwargs):
        super(Bcreateform,self).__init__(*args,**kwargs)
        self.label_suffix=''

class PostCreateform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["board_name","title","description","writer","date"]
        exclude = ['date',]
        widgets = {
            'title':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
            'description':forms.Textarea(attrs={'size':'100','style':'height:100;'}),
            'writer':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
        }
        labels = {"board_name":"만들 게시판 명","title":"제 목","description":"글 내용","writer":"작 성 자"}

    def __init__(self,*args,**kwargs):
        super(PostCreateform,self).__init__(*args,**kwargs)
        self.label_suffix=''   