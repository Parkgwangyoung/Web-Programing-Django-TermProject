from django.shortcuts import render,get_object_or_404
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from login.models import Student,Professor
from web.models import Board,BoardTable,Post
from django.urls import reverse
from web.forms import CreatePostform,BtCreateform,Bcreateform,PostCreateform,PostUpdateform
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
                student = Student.objects.all().exclude(name='관리자').order_by('student_number')
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
                student = Student.objects.all().exclude(name='관리자').order_by('student_number')
                professor = Professor.objects.all().order_by('name')
                return render(request,'web/assign.html',{'students':student,'professors':professor,'success':"지도교수배정성공"})
        except:
            try:
                if request.session.get('logined_special'):
                    student = Student.objects.all().exclude(name='관리자').order_by('student_number')
                    professor = Professor.objects.all().order_by('name')
                    return render(request,'web/assign.html',{'students':student,'professors':professor,'error':"지도교수배정실패"})
            except:
                return HttpResponse('잘못된 방향입니다.')
        

class BoardAccessView(View):
    def get(self,request,boardtable,*args,**kwargs):
        try:
            boardtables = get_object_or_404(BoardTable,pk=boardtable)       
            boards = boardtables.board_set.all()
            Bt = BoardTable.objects.all()
            return render(request,'web/board.html',{'board':boards,'pk':boardtable,'boardtable':Bt})
        except:
            return HttpResponse('올바르지않습니다.')

class BoardView(View):
    def get(self,request,boardtable,board,*args,**kwargs):
        try:
            boardtables =get_object_or_404(BoardTable,pk=boardtable)
            boards = boardtables.board_set.all()
            get_board = get_object_or_404(Board,pk=board)
            post = get_board.post_set.all()
            Bt = BoardTable.objects.all()
            return render(request,'web/board.html',{'post':post,'board':boards,'pk':boardtable,'ak':board,'boardtable':Bt})
        except:
            return HttpResponse('올바르지않습니다.')

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
                writer_email = student.email
                boards = get_object_or_404(Board,pk=board)
                for i  in boards.post_set.all():
                    board_name = i.board_name
                    break
                form = CreatePostform(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.writer =writer
                    post.writer_email = writer_email
                    post.board_name = board_name
                    post.save()
                    return HttpResponseRedirect(reverse('web:board',args=(boardtable,board,)))
            else:
                hidden = request.POST['professor_id']
                professor = Professor.objects.get(id = hidden)
                writer = professor.name
                writer_email = professor.email
                boards = get_object_or_404(Board,pk=board)
                for i  in boards.post_set.all():
                    board_name = i.board_name
                    break
                form = CreatePostform(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.writer =writer
                    post.writer_email = writer_email
                    post.board_name = board_name
                    post.save()
                    return HttpResponseRedirect(reverse('web:board',args=(boardtable,board,)))
        except:
            return HttpResponse('어드민이십니까?')

# 만약 포스트에 목록으로 들어가는창 혹은 뒤로가기 창이있으면 url이 바뀌어야함
class PostView(View):
    def get(self,request,post,*args,**kwargs):
        try: #학생의경우
            student_id = request.session['logined_student_id']
            student = Student.objects.get(id = student_id)
            email = student.email
            posts = get_object_or_404(Post,pk=post)
            return render(request,'web/post.html',{'post':posts,'email':email,'pk':post})
        except:  #교수의경우
            try:
                professor_id = request.session['logined_professor_id']
                professor = Professor.objects.get(id = professor_id)
                email = professor.email
                posts = get_object_or_404(Post,pk=post)
                return render(request,'web/post.html',{'post':posts,'email':email,'pk':post})
            except: #관리자의경우
                posts = get_object_or_404(Post,pk=post)
                return render(request,'web/post.html',{'post':posts,'pk':post})
        
#게시글 수정
class UpdatePostView(View):
    def get(self,request,post,*args,**kwargs):
        form = PostUpdateform()       
        return render(request,'web/updatepost.html',{'form':form,'pk':post})

    def post(self,request,post,*args,**kwargs):
        form = PostUpdateform(request.POST)
        if form.is_valid():
            try:                                     
                post_get = Post.objects.get(id=post)
                post_get = PostUpdateform(request.POST, instance=post_get)
                post_get.save(commit=False)
                post_get.save()
                return HttpResponseRedirect(reverse('web:post',args=(post,)))
            except:
                return HttpResponse('올바르지 않습니다.')

#게시글 삭제
class DeletePostView(View):
    def get(self,request,post,*args,**kwargs):
        posts = get_object_or_404(Post,pk=post)
        posts.delete()
        return HttpResponseRedirect(reverse('web:website'))

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
                return render(request,'web/createboardtable.html',{'Bform':form,'Btsuccess':"상위게시판생성완료"})             

class BcreateView(View):
    def get(self,request,*args,**kwargs):
        form = Bcreateform()
        return render(request,'web/createboardtable.html',{'Bform':form})


    def post(self,request,*args,**kwargs):
        form = Bcreateform(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            form =Bcreateform()
            return render(request,'web/createboardtable.html',{'Bform':form,'Bsuccess':"하위게시판생성완료"})

   

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
            form.professor = 1
            form.save()
            form = PostCreateform()
            return render(request,'web/createboardtable.html',{'Pform':form,'Psuccess':"게시글 작성완료"})



class likeView(View):
    def get(self,request,post,*args,**kwargs):
        try:
            posts = get_object_or_404(Post,pk=post)
            student = Student.objects.get(id = request.session['logined_student_id'])
            check_like_post = student.like_post.filter(id = post)

            if check_like_post.exists():
                student.like_post.remove(posts)
                posts.like_number -= 1
                posts.save()
            else:
                student.like_post.add(posts)
                posts.like_number += 1
                posts.save()
        
            return render(request,'web/post.html',{'post':posts,'pk':post,'success':" "})
        except:
            try:
                posts = get_object_or_404(Post,pk=post)
                professor = Professor.objects.get(id = request.session['logined_professor_id'])
                check_like_post = professor.like_post.filter(id = post)

                if check_like_post.exists():
                    professor.like_post.remove(posts)
                    posts.like_number -=1
                    posts.save()
                else:
                    professor.like_post.add(posts)
                    posts.like_number += 1
                    posts.save()
            
                return render(request,'web/post.html',{'post':posts,'pk':post,'success':" "})
            except:
                posts = get_object_or_404(Post,pk=post)
                return render(request,'web/post.html',{'post':posts,'pk':post,'error':" "})
