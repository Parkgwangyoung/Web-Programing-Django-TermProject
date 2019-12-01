from django.shortcuts import render,get_object_or_404
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from login.models import Student,Professor
from web.models import Board,BoardTable,Post
from django.urls import reverse
from web.forms import CreatePostform,BtCreateform,Bcreateform,PostCreateform
from django.core.exceptions import PermissionDenied
# Create your views here.

#메인홈페이지
class indexView(View):
    def get(self,request,*args,**kwargs):
        try:
            boardtable = BoardTable.objects.all()
            return render(request,'web/website.html',{'boardtable':boardtable})
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
                return render(request,'web/assign.html',{'students':student,'professors':professor})
        except:
            return HttpResponse('잘못된 방식입니다. 학생과 교수 둘다 선택되어있는지 확인해주세요.')
        

class BoardAccessView(View):
    def get(self,request,boardtable,*args,**kwargs):
        boardtables = get_object_or_404(BoardTable,pk=boardtable)       
        boards = boardtables.board_set.all()      
        return render(request,'web/board.html',{'board':boards,'pk':boardtable})

class BoardView(View):
    def get(self,request,boardtable,board,*args,**kwargs):
        boardtables =get_object_or_404(BoardTable,pk=boardtable)
        boards = boardtables.board_set.all()
        get_board = get_object_or_404(Board,pk=board)
        post = get_board.post_set.all()
        return render(request,'web/board.html',{'post':post,'board':boards,'pk':boardtable,'ak':board})

class CreatepostView(View):
    def get(self,request,boardtable,board,*args,**kwargs):
        form = CreatePostform()
        return render(request,'web/createpost.html',{'form':form,'ak':board,'pk':boardtable})
    

    def post(self,request,boardtable,board,*args,**kwargs):
        try:
            if request.session.get('logined_student_id'):
                hidden = request.POST['student_id']
                student = Student.objects.get(id = hidden)
                writer = student.name
                boards = get_object_or_404(Board,pk=board)
                for i  in boards.post_set.all():
                    board_name = i.board_name
                    break
                form = CreatePostform(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.writer =writer
                    post.board_name = board_name
                    post.save()
                    return HttpResponseRedirect(reverse('web:board',args=(boardtable,board,)))
            else:
                hidden = request.POST['professor_id']
                professor = Professor.objects.get(id = hidden)
                writer = professor.name
                boards = get_object_or_404(Board,pk=board)
                for i  in boards.post_set.all():
                    board_name = i.board_name
                    break
                form = CreatePostform(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.writer =writer
                    post.board_name = board_name
                    post.save()
                    return HttpResponseRedirect(reverse('web:board',args=(boardtable,board,)))
        except:
            return HttpResponse('어드민이십니까?')

# 만약 포스트에 목록으로 들어가는창 혹은 뒤로가기 창이있으면 url이 바뀌어야함
class PostView(View):
    def get(self,request,post,*args,**kwargs):
        post = get_object_or_404(Post,pk=post)
        return render(request,'web/post.html',{'post':post})



class BtcreateView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined_special'):
            form = BtCreateform()
            return render(request,'web/createboardtable.html',{'Btform':form})
        else:
            raise PermissionDenied

    def post(self,request,*args,**kwargs):
            form = BtCreateform(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.save()
                form =Bcreateform()
                return render(request,'web/createboardtable.html',{'Bform':form})             

class BcreateView(View):
    def post(self,request,*args,**kwargs):
        form = Bcreateform(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            form =Bcreateform()
            return render(request,'web/createboardtable.html',{'Bform':form})

   

class BpCreateView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined_special'):
            form = PostCreateform()
            return render(request,'web/createboardtable.html',{'Pform':form})
        else:
            raise PermissionDenied

    def post(self,request,*args,**kwargs):
        form = PostCreateform(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            form = PostCreateform()
            return render(request,'web/createboardtable.html',{'Pform':form})

def SelCreateBoard(request):
    return render(request, 'web/selCreateBoard.html')

class SecondBoardCreateView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined_special'):
            form = Bcreateform()
            return render(request,'web/secondBoard.html',{'Bform':form})
        else:
            raise PermissionDenied