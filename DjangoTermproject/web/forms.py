from django import forms
from django.forms import ModelForm
from web.models import BoardTable,Board,Post,Uploaded_File,Reply
from.import views

class CreatePostform(forms.ModelForm):
    class Meta:
        model = Post
        fileds = ["board_name","title","description","date","writer","writer_email","student","professor","like_number"]
        exclude = ['board_name','date','writer','writer_email','student','professor','like_number',]
        widgets = {
            'title':forms.TextInput(attrs={'size':'30','style':'height:35px;','placeholder':'제목을 입력하세요.'}),
            'description' : forms.Textarea(attrs={'size':'100','style':'height:100;width:100%'}),


        }
        labels = {"title":"","description":"내 용"}

    def __init__(self,*args,**kwargs):
        super(CreatePostform,self).__init__(*args,**kwargs)
        self.label_suffix=''

class BtCreateform(forms.ModelForm):
    class Meta:
        model = BoardTable
        fields = ["board_type",]
        widgets = {'board_type':forms.TextInput(attrs={'size':'30','style':'height:30;','placeholder':'여기에 입력'})}
        labels = {"board_type":"만들고 싶은 게시판 명 "}

    def __init__(self,*args,**kwargs):
        super(BtCreateform,self).__init__(*args,**kwargs)
        self.label_suffix=''

class Bcreateform(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["board_type","board_name","supervisor","grade"]
        widgets = {'board_name':forms.TextInput(attrs={'size':'30','style':'height:30;','placeholder':'여기에 입력'})
        ,'supervisor':forms.TextInput(attrs={'size':'30','style':'height:30;','placeholder':'여기에 입력'})
        ,'grade':forms.TextInput(attrs={'size':'30','style':'height:30;','placeholder':'여기에 입력'})
        }
        labels = {"board_name":"만들고 싶은 게시판 명 ","supervisor":"지도교수명(없을시 관리자로 쓰기)","grade":"학년(없을시 관리자로 쓰기)"}

    def __init__(self,*args,**kwargs):
        super(Bcreateform,self).__init__(*args,**kwargs)
        self.label_suffix=''

class PostCreateform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["board_name","title","description","writer","date","like_number","student","professor","writer_email"]
        exclude = ['date','student','professor','writer_email','like_number']
        widgets = {
            'title':forms.TextInput(attrs={'size':'30','style':'height:30;','placeholder':'여기에 제목'}),
            'description':forms.Textarea(attrs={'size':'20','style':'height:100; width:100%','placeholder':'여기에 글 내용'}),
            'writer':forms.TextInput(attrs={'size':'30','style':'height:30;','placeholder':'여기에 작성자'}),
        }
        labels = {"board_name":"게시판 명","title":"제 목","description":"글 내용","writer":"작 성 자"}

    def __init__(self,*args,**kwargs):
        super(PostCreateform,self).__init__(*args,**kwargs)
        self.label_suffix=''



class PostUpdateform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["board_name","title","description","writer","date","writer_email","student","professor","like_number"]
        exclude = ['date','writer','board_name','writer_email','student','professor','like_number']
        widgets = {
            'title':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
            'description':forms.Textarea(attrs={'size':'100','style':'height:100; width:100%'}),



        }
        labels = {"title":"","description":"내 용"}

    def __init__(self,*args,**kwargs):
        super(PostUpdateform,self).__init__(*args,**kwargs)
        self.label_suffix=''


class Replyform(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["post","reply","writer"]
        exclude = {'post','writer'}
        widgets = {
            'reply':forms.TextInput(attrs={'style':'height:30px; width:87%'}),
        }
        labels = {"reply":""}

    def __init__(self,*args,**kwargs):
        super(Replyform,self).__init__(*args,**kwargs)
        self.label_suffix=''
