from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from web.forms import StudentSigninForm,ProfessorSigninForm,StudentUpdateForm,ProfessorUpdateForm,Grade_TableForm,Professor_TableForm,Course_TableForm
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from web.models import Professor,Grade_Table,Professor_Table,Course_Table,Student

# 회원가입을 처리하는 뷰
class signinView(View):
    def get(self,request,pk,*args,**kwargs):
        if pk == 1:
            form =  StudentSigninForm()
            return render(request,'web/signin.html',{'studentform':form})
        else:
            form = ProfessorSigninForm()
            return render(request,'web/signin.html',{'professorform':form})
    
    def post(self,request,pk,*args,**kwargs):
        if pk == 1:
            form = StudentSigninForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.save()
                return HttpResponseRedirect(reverse('web:website'))
        else:
            form = ProfessorSigninForm(request.POST)
            if form.is_valid():
                professor = form.save(commit=False)
                professor.save()
                return HttpResponseRedirect(reverse('web:website'))


# 로그인을 처리하는 뷰
class loginView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined'):
            return HttpResponseRedirect(reverse('web:website'))
        else:
            return render(request,'web/login.html')

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
                    return render(request,'web/login.html',{'error':"계정 정보가 맞지 않습니다"})   
            except:
                try:
                    professor = Professor.objects.get(email=get_email)
                    if professor.password == get_password:
                        request.session['logined'] = professor.name
                        request.session['logined_professor_id'] = professor.id
                        return HttpResponseRedirect(reverse('web:website'))
                    else:                       
                        return render(request,'web/login.html',{'error':"계정 정보가 맞지 않습니다"})
                except:                
                    return render(request,'web/login.html',{'error':"계정 정보가 맞지 않습니다"})                      
        else:
            return render(request,'web/login.html',{'error':"계정 정보가 맞지 않습니다"})

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
        return render(request,'web/update.html',{'form':form})
    
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
                        return render(request,'web/update.html',{'form':form,'error':"기존비밀번호를 잘못입력하셨습니다."})
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
                        return render(request,'web/update.html',{'form':form,'error':"기존비밀번호를 잘못입력하셨습니다."})
                except:
                    return HttpResponse('잘못된 경로입니다.')

# 지도교수를 배정하는 뷰
class assignView(View):
    def get(self,request,*args,**kwargs):
        try:
            student = Student.objects.all().exclude(name='admin').order_by('student_number')
            professor = Professor.objects.all().order_by('name')
            return render(request,'web/assign.html',{'students':student,'professors':professor})
        except:
            return HttpResponse('잘못된 방향입니다.')

    def post(self,request,*args,**kwargs):
        try:
            professor_get = Professor.objects.get(id=request.POST['professor'])
            student_get = Student.objects.get(id=request.POST['student'])
            student_get.tutor = professor_get.name 
            student_get.save()
            student = Student.objects.all().exclude(name='admin').order_by('student_number')
            professor = Professor.objects.all().order_by('name')
            return render(request,'web/assign.html',{'students':student,'professors':professor})
        except:
            return HttpResponse('잘못된 방식입니다. 학생과 교수 둘다 선택되어있는지 확인해주세요.')
        

#게시판 창 띄워주는 뷰
class BoardView(View):
    def get(self,request,pk,tk,*args,**kwargs):
        try:
            if pk == 1:
                grade_post = Grade_Table.objects.all().filter(grade = tk)
                return render(request,'web/grade_board.html',{'Gtable':grade_post,'id':pk,'grade':tk})
            elif pk == 2:
                if request.session.get('logined_student_id'):
                    student = Student.objects.get(id = request.session['logined_student_id'])
                    tutor = student.tutor
                    professor_post = Professor_Table.objects.all().filter(professor_name = tutor)
                    return render(request,'web/professor_board.html',{'Ptable':professor_post,'id':pk,'tutor':tutor,'grade':tk})
                else:
                    professor = Professor.objects.get(id = request.session['logined_professor_id'])
                    professor_post = Professor_Table.objects.all().filter(professor_name = professor.name)
                    return render(request,'web/professor_board.html',{'Ptable':professor_post,'id':pk,'name':professor.name})
            else:
                course_post = Course_Table.objects.get(id=tk)
                return render(request,'web/course_board.html',{'Ctable':course_post,'id':pk,'grade':tk})
        except:
            return HttpResponse('잘못된 경로입니다.')
        

# 게시판 창에서 글쓰기 버튼을 눌렀을때 처리되는 뷰 ( 글 쓰기 폼 )
class Create_PostView(View):
    def get(self,request,pk,tk,*args,**kwargs):
        if pk == 1:
            form = Grade_TableForm()
            return render(request,'web/grade_createpost.html',{'form':form,'id':pk,'grade':tk})
        elif pk == 2:
            form = Professor_TableForm()
            return render(request,'web/professor_createpost.html',{'form':form,'id':pk})
        else:
            form = Course_TableForm()
            return render(request,'web/course_createpost.html',{'form':form,'id':pk})
# 세션을 이용해서 작성자를 출력하도록해야함
    def post(self,request,pk,tk,*args,**kwargs):     
        try:
            if pk == 1:
                if request.session.get('logined_student_id'):      
                    hidden = request.POST['student_id']
                    student = Student.objects.get(id=hidden)
                    writer = student.name
                    grade = student.grade
                    form = Grade_TableForm(request.POST)
                    if form.is_valid():
                        grade_table = form.save(commit=False)
                        grade_table.writer = writer
                        grade_table.grade = grade
                        grade_table.save()
                        return HttpResponseRedirect(reverse('web:board',args=(pk,tk,)))
                else:
                    hidden = request.POST['professor_id']
                    professor = Professor.objects.get(id = hidden)
                    writer = professor.name
                    grade = tk
                    form = Grade_TableForm(request.POST)
                    if form.is_valid():
                        grade_table = form.save(commit=False)
                        grade_table.writer = writer
                        grade_table.grade = grade
                        grade_table.save()
                        return HttpResponseRedirect(reverse('web:board',args=(pk,tk,)))
            elif pk == 2:
                if request.session.get('logined_student_id'):
                    hidden = request.POST['student_id']
                    student = Student.objects.get(id=hidden)
                    tutor = student.tutor
                    writer = student.name
                    form = Professor_TableForm(request.POST)
                    if form.is_valid():
                        professor_table = form.save(commit=False)
                        professor_table.writer = writer
                        professor_table.professor_name = tutor
                        professor_table.save()
                        return HttpResponseRedirect(reverse('web:board',args=(pk,tk)))
                else:
                    hidden = request.POST['professor_id']
                    professor = Professor.objects.get(id=hidden)
                    form = Professor_TableForm(request.POST)
                    if form.is_valid():
                        professor_table = form.save(commit=False)
                        professor_table.writer = professor.name
                        professor_table.professor_name = professor.name
                        professor_table.save()
                        return HttpResponseRedirect(reverse('web:board',args=(pk,tk)))
            else:
                writer = request.POST['writer']
                form = Course_TableForm(request.POST)
                if form.is_valid():
                    course_table = form.save(commit=False)
                    course_table.writer = writer
                    course_table.save()
                    return HttpResponseRedirect(reverse('web:board',args=(pk,)))
        except:
            raise PermissionDenied


# 게시판창에서 특정글을 눌렀을때 글의 내용이나오는 뷰
class BoardAccessView(View):
    def get(self,request,pk,tk,ak,*args,**kwargs):
        try:
            if pk == 1:
                grade_post = Grade_Table.objects.get(id=ak)
                return render(request,'web/grade_post.html',{'post':grade_post})
            elif pk == 2:
                professor_post = Professor_Table.objects.get(id=ak)
                return render(request,'web/professor_post.html',{'post':professor_post})
            else:
                course_post = Course_Table.objects.get(id=ak)
                return render(request,'web/course_post.html',{'post':course_post})
        except:
            return HttpResponse('잘못된 경로입니다.')


# 학생들이 만들고 싶은 게시판을 요청할 수 있다.
class reqireView(View):
    def get(self,request,pk,tk,*args,**kwargs):
        return render(request,'web/reqire.html')
    def post(self,request,pk,tk,*args,**kwargs):
        return HttpResponse('hello')

class TestBranchView(View):
    def get(self,request,pk,tk,*args,**kwargs):
        return render(request,'web/reqire.html')
    def post(self,request,pk,tk,*args,**kwargs):
        return HttpResponse('hello')

