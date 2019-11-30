from django import forms
from login.models import Student,Professor


class StudentSigninForm(forms.ModelForm):

    class Meta:
        model = Student
        labels = {"name":"성  함","email":"아 이 디","password":"비밀번호","grade":"학  년","student_number":"학  번"}
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
        labels = {"name":"성  함","email":"아 이 디","password":"비밀번호","professor_number":"직원번호"}
        fields = ["name","email","password","professor_number"]
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
        labels={"name" : "성  함","student_number":"학  번","password":"새 비밀번호",
         }
         
    def __init__(self,*args,**kwargs):
        super(StudentUpdateForm,self).__init__(*args,**kwargs)
        self.label_suffix=''
        self.fields['root_password'].label='현재 비밀번호'

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
        labels={"name" : "성  함","student_number":"직 원 번 호　","password":"새 비밀번호",
         }
         
    def __init__(self,*args,**kwargs):
        super(ProfessorUpdateForm,self).__init__(*args,**kwargs)
        self.label_suffix=''
        self.fields['root_password'].label='현재 비밀번호'