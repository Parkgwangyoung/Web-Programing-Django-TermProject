from django.shortcuts import render,get_object_or_404
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from login.models import Student,Professor
from web.models import Board,BoardTable
from web.forms import CreatePostform,BtCreateform,Bcreateform
from django.urls import reverse
# Create your views here.

#메인홈페이지
class indexView(View):
    def get(self,request,*args,**kwargs):
        try:
            board = BoardTable.objects.all()
            return render(request,'web/website.html',{'boards':board})
        except:
            return HttpResponse('올바르지 않습니다.')

# 지도교수를 배정하는 뷰
class assignView(View):
    def get(self,request,*args,**kwargs):
        try:
            if request.session.get('logined_special'):
                student = Student.objects.all().exclude(name='admin').order_by('student_number')
                professor = Professor.objects.all().order_by('name')
                return render(request,'web/assign.html',{'students':student,'professors':professor})
            else:
                return HttpResponse('잘못된 방향입니다.')
        except:
            return HttpResponse('잘못된 방향입니다.')

    def post(self,request,*args,**kwargs):
        try:
            if request.session.get('logined_special'):
                professor_get = Professor.objects.get(id=request.POST['professor'])
                student_get = Student.objects.get(id=request.POST['student'])
                student_get.tutor = professor_get.name 
                student_get.save()
                student = Student.objects.all().exclude(name='admin').order_by('student_number')
                professor = Professor.objects.all().order_by('name')
                return render(request,'web/assign.html',{'students':student,'professors':professor,'success':"성공"})
        except:
            return HttpResponse('잘못된 방식입니다. 학생과 교수 둘다 선택되어있는지 확인해주세요.')
        
#게시판 창화면
class BoardView(View):

    def get(self,request,board,*args,**kwargs):
        boards = get_object_or_404(BoardTable,pk=board)
        return render(request,'web/board.html',{'board':boards,'pk':board})

# 게시글 글쓰기
class CreateView(View):
    def get(self,request,board,*args,**kwargs):
        form = CreatePostform()
        return render(request,'web/createpost.html',{'form':form,'pk':board})

    def post(self,request,board,*args,**kwars):
        try:
            if request.session.get('logined_student_id'):
                hidden = request.POST['student_id']
                student = Student.objects.get(id = hidden)
                writer = student.name
                boards = get_object_or_404(BoardTable,pk=board)
                for i in boards.board_set.all():
                    board_type = i.board_type
                    break
                form = CreatePostform(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.writer = writer
                    post.board_type = board_type
                    post.save()
                    return HttpResponseRedirect(reverse('web:board',args=(board,)))
            else:
                hidden = request.POST['professor_id']
                professor = Professor.objects.get(id = hidden)
                writer = professor.name
                boards = get_object_or_404(BoardTable,pk=board)
                for i in boards.board_set.all():
                    board_type = i.board_type
                    break
                form = CreatePostform(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.writer = writer
                    post.board_type = board_type
                    post.save()
                    return HttpResponseRedirect(reverse('web:board',args=(board,)))
                
        except:
            return HttpResponse('올바르지 않습니다.')

#게시글 열람    
class postView(View):
    def get(self,request,board,*args,**kwargs):
        board = get_object_or_404(Board,pk=board)
        return render(request,'web/post.html',{'board':board})

#게시판생성
class BtCreateView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined_special'):
            sform = BtCreateform()
            return render(request,'web/createboardtable.html',{'sform':sform})
    
    def post(self,request,*args,**kwargs):
            form = BtCreateform(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.save()
                gform = Bcreateform()
                return render(request,'web/createboardtable.html',{'gform':gform})

#게시판생성
class BtAccessView(View):
    def post(self,request,*args,**kwargs):
        form = Bcreateform(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            sform = BtCreateform()
            return render(request,'web/createboardtable.html',{'sform':sform})