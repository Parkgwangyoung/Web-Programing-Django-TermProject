from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from login.forms import StudentSigninForm,StudentUpdateForm,ProfessorSigninForm,ProfessorUpdateForm
from login.models import Student,Professor
# Create your views here.


# 회원가입을 처리하는 뷰
class signinView(View):
    def get(self,request,pk,*args,**kwargs):
        if pk == 1:
            form =  StudentSigninForm()
            return render(request,'login/signin.html',{'studentform':form})
        else:
            form = ProfessorSigninForm()
            return render(request,'login/signin.html',{'professorform':form})
    
    def post(self,request,pk,*args,**kwargs):
        if pk == 1:
            form = StudentSigninForm(request.POST)
            if form.is_valid():
                g_email = form.cleaned_data['email']
                g_grade = form.cleaned_data['grade']
                try: 
                    if g_grade == '1' or g_grade =='2' or g_grade =='3' or g_grade =='4':
                        Student.objects.get(email= g_email)                   
                        return render(request,'login/signin.html',{'studentform':form,'error2':"계정존재"})                       
                    else:
                        return render(request,'login/signin.html',{'studentform':form,'error3':"학년"})
                except:
                    try:
                        Professor.objects.get(email = g_email)
                        return render(request,'login/signin.html',{'studentform':form,'error2':"계정존재"})
                    except:
                        student = form.save(commit=False)
                        student.save()
                        return HttpResponseRedirect(reverse('web:website'))
            else:
                form =  StudentSigninForm()
                return render(request,'login/signin.html',{'studentform':form,'error':"이메일"})
        else:
            form = ProfessorSigninForm(request.POST)
            if form.is_valid():
                g_email = form.cleaned_data['email']
                try:
                    Professor.objects.get(email = g_email)
                    return render(request,'login/signin.html',{'professorform':form,'error2':"계정존재"})
                except:
                    try:
                        Student.objects.get(email= g_email)
                        return render(request,'login/signin.html',{'professorform':form,'error2':"계정존재"})
                    except:
                        professor = form.save(commit=False)
                        professor.save()
                        return HttpResponseRedirect(reverse('web:website'))
            else:
                form = ProfessorSigninForm()
                return render(request,'login/signin.html',{'professorform':form,'error':"이메일"})


# 로그인을 처리하는 뷰
class loginView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined'):
            return HttpResponseRedirect(reverse('web:website'))
        else:
            return render(request,'login/login.html')

    def post(self,request,*args,**kwargs):
        get_email = request.POST['email']
        get_password = request.POST['password']
        if get_email and get_password:
            try:
                student = Student.objects.get(email=get_email)
                if student.password == get_password:
                    request.session['logined'] = student.name
                    if student.id == 1:
                        request.session['logined_special'] = student.id
                        return HttpResponseRedirect(reverse('web:website'))
                    else:
                        request.session['logined_student_id'] = student.id
                        request.session['logined_student_grade'] = student.grade
                        return HttpResponseRedirect(reverse('web:website'))                    
                else:
                    # return HttpResponse(1)
                    return render(request,'login/login.html',{'error2':"패스워드미스"})   
            except:
                try:
                    professor = Professor.objects.get(email=get_email)
                    if professor.password == get_password:
                        request.session['logined'] = professor.name
                        request.session['logined_professor_id'] = professor.id
                        return HttpResponseRedirect(reverse('web:website'))
                    else:                       
                        return render(request,'login/login.html',{'error2':"패스워드미스"})
                except:                
                    return render(request,'login/login.html',{'error3':"계정이 존재하지않음"})                      
        else:
            return render(request,'login/login.html',{'error':"잘못된 접근"})


# 로그아웃을 처리하는 뷰          
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        if not request.session.get('logined_student_id'):
            if not request.session.get('logined_professor_id'):
                if not request.session.get('logined_special'):
                    raise PermissionDenied
                del request.session['logined']
                del request.session['logined_special']
                return HttpResponseRedirect(reverse('web:website'))
            del request.session['logined']
            del request.session['logined_professor_id']
            return HttpResponseRedirect(reverse('web:website'))
        del request.session['logined']
        del request.session['logined_student_id']
        del request.session['logined_student_grade']
        return HttpResponseRedirect(reverse('web:website'))


# 회원정보를 변경하는 뷰
class updateView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined_student_id'):
            form = StudentUpdateForm()
        else:
            form = ProfessorUpdateForm()
        return render(request,'login/update.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        if request.session.get('logined_student_id'):
            form = StudentUpdateForm(request.POST)
            if form.is_valid():
                hidden = request.POST['id']
                root_password = form.cleaned_data['root_password']
                try:
                    student_get = Student.objects.get(id=hidden)
                    if student_get.password == root_password:
                        student = StudentUpdateForm(request.POST, instance=student_get)
                        student.save()
                        request.session['logined'] = form.cleaned_data['name']
                        return HttpResponseRedirect(reverse('web:website'))
                    else:
                        form = StudentUpdateForm()
                        return render(request,'login/update.html',{'form':form,'error':"기존비밀번호미스"})
                except:
                    return HttpResponse('잘못된 경로입니다.')
        else:
            form = ProfessorUpdateForm(request.POST)
            if form.is_valid():
                hidden = request.POST['id']
                root_password = form.cleaned_data['root_password']
                try:
                    professor_get = Professor.objects.get(id=hidden)
                    if professor_get.password == root_password:
                        professor = ProfessorUpdateForm(request.POST, instance=professor_get)
                        professor.save()
                        request.session['logined'] = form.cleaned_data['name']
                        return HttpResponseRedirect(reverse('web:website'))
                    else:
                        form = ProfessorUpdateForm()
                        return render(request,'login/update.html',{'form':form,'error':"기존비밀번호미스"})
                except:
                    return HttpResponse('잘못된 경로입니다.')