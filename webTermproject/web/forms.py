from django import forms
from web.models import Student,Professor,Table,Grade_Table,Professor_Table,Course_Table
from django.forms import ModelForm,Textarea

class StudentSigninForm(forms.ModelForm):

    class Meta:
        model = Student
        labels = {"name":"성  함","email":"아 이 디","student_number":"학  번","password":"비밀번호"}
        fields = ["name","email","password","grade","student_number","tutor"]
        exclude = ['tutor',]
        widgets = { 'password': forms.PasswordInput(attrs={'size':'30','style':'height:30;'},),
                    'name' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
                    'email' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
                    'student_number' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
                    'grade':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
                    
                    }
      

    def __init__(self,*args,**kwargs):
        super(StudentSigninForm,self).__init__(*args,**kwargs)
        self.label_suffix=''

class ProfessorSigninForm(forms.ModelForm):

    class Meta:
        model = Professor
        labels = {"name":"성  함","email":"아 이 디","professor_number":"직원번호","password":"비밀번호"}
        fields = ["name","email","professor_number","password"]
        widgets = { 'password': forms.PasswordInput(attrs={'size':'30','style':'height:30;'}),
                    'name' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
                    'email' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
                    'professor_number' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
                    }
        

    def __init__(self,*args,**kwargs):
        super(ProfessorSigninForm,self).__init__(*args,**kwargs)
        self.label_suffix=''


class StudentUpdateForm(forms.ModelForm):
    root_password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'size':'30','style':'height:30;'}))
    class Meta:
        model = Student
        fields = ["name","email","student_number","root_password","password","tutor"]
        exclude = ['email',"tutor",]
        widgets = { 
            
            'password': forms.PasswordInput(attrs={'size':'30','style':'height:30;'}),
            'name' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
            'student_number' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
            }
        labels={"name" : "성　　　함　","student_number":"학　　　번　","password":"변경후 비밀번호",
         }
         
    def __init__(self,*args,**kwargs):
        super(StudentUpdateForm,self).__init__(*args,**kwargs)
        self.label_suffix=''
        self.fields['root_password'].label='변경전 비밀번호'

class ProfessorUpdateForm(forms.ModelForm):
    root_password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'size':'30','style':'height:30;'}))
    class Meta:
        model = Professor
        fields = ["name","email","professor_number","root_password","password"]
        exclude = ['email',]
        widgets = { 
            
            'password': forms.PasswordInput(attrs={'size':'30','style':'height:30;'}),
            'name' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
            'professor_number' : forms.TextInput(attrs={'size':'30','style':'height:30;'}),
            }
        labels={"name" : "성　　　함　","student_number":"직 원 번 호　","password":"변경후 비밀번호",
         }
         
    def __init__(self,*args,**kwargs):
        super(ProfessorUpdateForm,self).__init__(*args,**kwargs)
        self.label_suffix=''
        self.fields['root_password'].label='변경전 비밀번호'

# 학년을 알려면 모델의 필드중에 학년을 추가해야할듯
class Grade_TableForm(forms.ModelForm):
    class Meta:
        model = Grade_Table
        fields = ["grade","title","description","date"]
        exclude =['date','grade',]
        widgets = {
           'title':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
           'description': forms.Textarea(attrs={'size':'100','style':'height:100;'}),
        }
        labels = {"title":"제 목","description":"내 용"}

    def __init__(self,*args,**kwargs):
        super(Grade_TableForm,self).__init__(*args,**kwargs)
        self.label_suffix=''


class Professor_TableForm(forms.ModelForm):
    class Meta:
        model = Professor_Table
        fields = ["professor_name","title","description","date"]
        exclude =['date','professor_name',]
        widgets = {
           'title':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
           'description': forms.Textarea(attrs={'size':'100','style':'height:100;'}),
        }
        labels = {"title":"제 목","description":"내 용"}

    def __init__(self,*args,**kwargs):
        super(Professor_TableForm,self).__init__(*args,**kwargs)
        self.label_suffix=''

class Course_TableForm(forms.ModelForm):
    class Meta:
        model = Course_Table
        fields = ["course_name","title","description","date"]
        exclude =['date','course_name',]
        widgets = {
           'title':forms.TextInput(attrs={'size':'30','style':'height:30;'}),
           'description': forms.Textarea(attrs={'size':'100','style':'height:100;'}),
        }
        labels = {"title":"제 목","description":"내 용"}

    def __init__(self,*args,**kwargs):
        super(Course_TableForm,self).__init__(*args,**kwargs)
        self.label_suffix=''