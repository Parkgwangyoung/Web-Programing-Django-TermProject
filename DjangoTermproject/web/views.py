from django.shortcuts import render,get_object_or_404
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from login.models import Student,Professor
from web.models import Board,BoardTable,Post,Uploaded_File,Reply
from django.urls import reverse
from web.forms import CreatePostform,BtCreateform,Bcreateform,PostCreateform,PostUpdateform,Replyform
from django.core.exceptions import PermissionDenied
import itertools
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


# 게시판 클래스 뷰
class BoardAccessView(View):
    def get(self,request,boardtable,*args,**kwargs):
        if request.session.get('logined_student_id'): #학생이면
            try:    # 상위게시판명과 하위게시판명이 동일한 게시판을 열었을 경우, 즉 하위 분류가 없을경우 !!
                boardtables = get_object_or_404(BoardTable,pk=boardtable)
                board_name = boardtables.board_type
                boards_all = boardtables.board_set.all()
                boards_get = boardtables.board_set.get(board_name = board_name)
                request_name = boards_get.board_name
                ak = boards_get.id
                post = boards_get.post_set.all()
                Bt = BoardTable.objects.all()
                return render(request,'web/board.html',{'boards_get':boards_get,'post':post,'board':boards_all,'pk':boardtable,'ak':ak,'boardtable':Bt,'request_name':request_name})
            except:
                try: # 학생이 학년별게시판에 들어갈 때 검사하는곳
                    boardtables = get_object_or_404(BoardTable,pk=boardtable)
                    boards_all = boardtables.board_set.all()
                    boards_get = boardtables.board_set.get(grade = request.session['logined_student_grade'])
                    grade = boards_get.grade
                    ak = boards_get.id
                    post = boards_get.post_set.all()
                    Bt = BoardTable.objects.all()
                    return render(request,'web/board.html',{'boards_get':boards_get,'post':post,'board':boards_all,'pk':boardtable,'ak':ak,'boardtable':Bt,'grades':grade})
                except: #학생인데 학년별게시판에 들어가지않는 경우
                    try: #학생인데 지도교수 게시판에 들어가거나 혹은 다른게시판에 들어가는경우,
                        if request.session.get('logined_student_tutor'): #지도교수 배정이 되어있는경우,
                            boardtables = get_object_or_404(BoardTable,pk=boardtable)
                            boards_all = boardtables.board_set.all()
                            boards_get = boardtables.board_set.get(supervisor = request.session['logined_student_tutor'])
                            supervisor = boards_get.supervisor
                            ak = boards_get.id
                            post = boards_get.post_set.all()
                            Bt = BoardTable.objects.all()
                            return render(request,'web/board.html',{'boards_get':boards_get,'post':post,'board':boards_all,'pk':boardtable,'ak':ak,'boardtable':Bt,'supervisors':supervisor})
                        elif not request.session.get('logined_student_tutor'): #학생이지만 지도교수 배정이 이루어지지 않은경우
                            try:
                                boardtables = get_object_or_404(BoardTable,pk=boardtable)
                                board_type = boardtables.board_type
                                boards = boardtables.board_set.all()
                                Bt = BoardTable.objects.all()
                                return render(request,'web/board.html',{'board':boards,'pk':boardtable,'boardtable':Bt,'name':board_type})
                            except:
                                return HttpResponse('올바르지않습니다.')

                    except: # 튜터가 있는사람이 지도교수게시판에도 들어가지않는경우,
                        try:
                            boardtables = get_object_or_404(BoardTable,pk=boardtable)
                            board_type = boardtables.board_type
                            boards = boardtables.board_set.all()
                            Bt = BoardTable.objects.all()
                            return render(request,'web/board.html',{'board':boards,'pk':boardtable,'boardtable':Bt,'name':board_type})
                        except:
                            return HttpResponse('올바르지않습니다.')
        elif request.session.get('logined_professor_id'): #교수이면
            try:    #교수인 경우에 지도교수 게시판에 자기이름과 동일한 지도교수게시판으로 열람할 때
                boardtables = get_object_or_404(BoardTable,pk=boardtable)
                boards_all = boardtables.board_set.all()
                boards_get = boardtables.board_set.get(supervisor = request.session['logined'])
                supervisor = boards_get.supervisor
                ak = boards_get.id
                post = boards_get.post_set.all()
                Bt = BoardTable.objects.all()
                return render(request,'web/board.html',{'boards_get':boards_get,'post':post,'board':boards_all,'pk':boardtable,'ak':ak,'boardtable':Bt,'supervisors':supervisor})
            except: # 교수가 지도교수게시판을 열람하지 않은경우
                try: # 교수가 상위게시판명과 하위게시판명이 동일한 게시판을 열었을 경우, 즉 하위 분류가 없을경우 !!
                    boardtables = get_object_or_404(BoardTable,pk=boardtable)
                    board_name = boardtables.board_type
                    boards_all = boardtables.board_set.all()
                    boards_get = boardtables.board_set.get(board_name = board_name)
                    request_name = boards_get.board_name
                    ak = boards_get.id
                    post = boards_get.post_set.all()
                    Bt = BoardTable.objects.all()
                    return render(request,'web/board.html',{'boards_get':boards_get,'post':post,'board':boards_all,'pk':boardtable,'ak':ak,'boardtable':Bt,'request_name':request_name})
                except: # 교수가 지도교수게시판,요청게시판을 열람하지 않은경우
                    try:
                        boardtables = get_object_or_404(BoardTable,pk=boardtable)
                        board_type = boardtables.board_type
                        boards = boardtables.board_set.all()
                        Bt = BoardTable.objects.all()
                        return render(request,'web/board.html',{'board':boards,'pk':boardtable,'boardtable':Bt,'name':board_type})
                    except:
                        return HttpResponse('올바르지않습니다.')
        else: # 관리자인경우
            try:  #관리자가 상위게시판명과 하위게시판명이 동일한 게시판을 열었을 경우, 즉 하위 분류가 없을경우 !!
                boardtables = get_object_or_404(BoardTable,pk=boardtable)
                board_name = boardtables.board_type
                boards_all = boardtables.board_set.all()
                boards_get = boardtables.board_set.get(board_name = board_name)
                request_name = boards_get.board_name
                ak = boards_get.id
                post = boards_get.post_set.all()
                Bt = BoardTable.objects.all()
                return render(request,'web/board.html',{'boards_get':boards_get,'post':post,'board':boards_all,'pk':boardtable,'ak':ak,'boardtable':Bt,'request_name':request_name})
            except:
                try:
                    boardtables = get_object_or_404(BoardTable,pk=boardtable)
                    board_type = boardtables.board_type
                    boards = boardtables.board_set.all()
                    Bt = BoardTable.objects.all()
                    return render(request,'web/board.html',{'board':boards,'pk':boardtable,'boardtable':Bt,'name':board_type})
                except:
                    return HttpResponse('올바르지않습니다.')

# 게시판 뷰
class BoardView(View):
    def get(self,request,boardtable,board,*args,**kwargs):
        try:
            boardtables =get_object_or_404(BoardTable,pk=boardtable)
            boards = boardtables.board_set.all()
            get_board = get_object_or_404(Board,pk=board)
            name = get_board.board_name
            post = get_board.post_set.all()
            Bt = BoardTable.objects.all()
            return render(request,'web/board.html',{'post':post,'board':boards,'pk':boardtable,'ak':board,'boardtable':Bt,'name':name})
        except:
            return HttpResponse('올바르지않습니다.')

# 게시글 작성 클래스 뷰
class CreatepostView(View):
    def get(self,request,boardtable,board,*args,**kwargs):
        try:
            form = CreatePostform()
            Bt = BoardTable.objects.all()
            return render(request,'web/createpost.html',{'form':form,'ak':board,'pk':boardtable,'boardtable':Bt})
        except:
            return HttpResponse('올바르지 않습니다.')

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
                    if request.FILES.getlist('file'):
                        for file in request.FILES.getlist('file'):
                            try:
                                Uploaded_File.objects.create(post=post,file=file,writer=writer)
                            except:
                                return HttpResponse('올바르지 않습니다.')
                        return HttpResponseRedirect(reverse('web:board',args=(boardtable,board,)))
                    else:
                        return HttpResponseRedirect(reverse('web:board',args=(boardtable,board,)))
                else:
                    form = CreatePostform()
                    Bt = BoardTable.objects.all()
                    return render(request,'web/createpost.html',{'boardtable':Bt,'form':form,'ak':board,'pk':boardtable,'error':"글 미입력"})
            else:
                hidden = request.POST['professor_id']
                professor = Professor.objects.get(id = hidden)
                writer = professor.name
                writer_email = professor.email
                boards = get_object_or_404(Board,pk=board)
                for i  in boards.post_set.all():
                    board_name = i.board_name
                    break
                form = CreatePostform(request.POST,request.FILES)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.writer =writer
                    post.writer_email = writer_email
                    post.board_name = board_name
                    post.save()
                    if request.FILES.getlist('file'):
                        for file in request.FILES.getlist('file'):
                            try:
                                Uploaded_File.objects.create(post=post,file=file,writer=writer)
                            except:
                                return HttpResponse('올바르지 않습니다.')
                        return HttpResponseRedirect(reverse('web:board',args=(boardtable,board,)))
                    else:
                        return HttpResponseRedirect(reverse('web:board',args=(boardtable,board,)))
                else:
                    form = CreatePostform()
                    Bt = BoardTable.objects.all()
                    return render(request,'web/createpost.html',{'boardtable':Bt,'form':form,'ak':board,'pk':boardtable,'error':"글 미입력"})

        except:
            return HttpResponse('어드민이십니까?')

# 게시글 열람 클래스 뷰
class PostView(View):
    def get(self,request,post,*args,**kwargs):
        try: #학생의경우
            student_id = request.session['logined_student_id']
            student = Student.objects.get(id = student_id)
            email = student.email
            posts = get_object_or_404(Post,pk=post)
            files = posts.uploaded_file_set.all()
            reply = posts.reply_set.all()
            form = Replyform()
            Bt = BoardTable.objects.all()
            return render(request,'web/post.html',{'post':posts,'email':email,'pk':post,'files':files,'replyform':form,'reply':reply,'boardtable':Bt})
        except:  #교수의경우
            try:
                professor_id = request.session['logined_professor_id']
                professor = Professor.objects.get(id = professor_id)
                email = professor.email
                posts = get_object_or_404(Post,pk=post)
                files = posts.uploaded_file_set.all()
                reply = posts.reply_set.all()
                form = Replyform()
                Bt = BoardTable.objects.all()
                return render(request,'web/post.html',{'post':posts,'email':email,'pk':post,'files':files,'replyform':form,'reply':reply,'boardtable':Bt})
            except: #관리자의경우
                try:
                    posts = get_object_or_404(Post,pk=post)
                    files = posts.uploaded_file_set.all()
                    reply = posts.reply_set.all()
                    form = Replyform()
                    Bt = BoardTable.objects.all()
                    return render(request,'web/post.html',{'post':posts,'pk':post,'files':files,'replyform':form,'reply':reply,'boardtable':Bt})
                except:
                    return HttpResponse('올바르지 않습니다.')


# 댓글 작성 클래스 뷰
class ReplyView(View):
    def post(self,request,post,*args,**kwargs):
        try:
            if request.session.get('logined_student_id'):
                student = Student.objects.get(id= request.session['logined_student_id'])
                get_post = get_object_or_404(Post,pk=post)
                form = Replyform(request.POST)
                if form.is_valid():
                    reply = form.save(commit=False)
                    reply.post = get_post
                    reply.writer = student.name
                    reply.writer_email = student.email
                    reply.save()
                    return HttpResponseRedirect(reverse('web:post',args=(post,)))
            elif request.session.get('logined_professor_id'):
                professor = Professor.objects.get(id = request.session['logined_professor_id'])
                get_post = get_object_or_404(Post,pk=post)
                form = Replyform(request.POST)
                if form.is_valid():
                    reply = form.save(commit=False)
                    reply.post = get_post
                    reply.writer = professor.name
                    reply.writer_email = professor.email
                    reply.save()
                    return HttpResponseRedirect(reverse('web:post',args=(post,)))
            else:
                admin = Student.objects.get(id = 1)
                get_post = get_object_or_404(Post,pk=post)
                form = Replyform(request.POST)
                if form.is_valid():
                    reply = form.save(commit=False)
                    reply.post = get_post
                    reply.writer = admin.name
                    reply.save()
                    return HttpResponseRedirect(reverse('web:post',args=(post,)))
        except:
            return HttpResponse('올바르지않습니다.')

# 댓글 수정 클래스 뷰
class ReplyUpdateView(View):
    def get(self,request,post,reply,*args,**kwargs):
        try:
            posts = get_object_or_404(Post,pk=post)
            form = Replyform()
            files = posts.uploaded_file_set.all()
            reply_all = posts.reply_set.all()
            Bt = BoardTable.objects.all()
            return render(request,'web/post.html',{'replyupdateform':form,'pk':post,'rk':reply,'post':posts,'reply':reply_all,'files':files,'replyform':form,'boardtable':Bt})
        except:
            return HttpResponse('올바르지않습니다.')

    def post(self,request,post,reply,*args,**kwargs):
        get_reply = get_object_or_404(Reply,pk=reply)
        form = Replyform(request.POST,instance=get_reply)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web:post',args=(post,)))

#댓글 삭제 클래스 뷰
class ReplyDeleteView(View):
    def get(self,request,post,reply,*args,**kwargs):
        get_reply = get_object_or_404(Reply,pk=reply)
        get_reply.delete()
        return HttpResponseRedirect(reverse('web:post',args=(post,)))


#게시글 수정 클래스 뷰
class UpdatePostView(View):
    def get(self,request,post,*args,**kwargs):
        try:
            get_post = get_object_or_404(Post,pk=post)
            Bt = BoardTable.objects.all()
            form = PostUpdateform(initial={'title':get_post.title,'description':get_post.description})
            return render(request,'web/updatepost.html',{'form':form,'pk':post,'boardtable':Bt,})
        except:
            return HttpResponse('올바르지 않습니다.')

    def post(self,request,post,*args,**kwargs):
        try:
            post_get = Post.objects.get(id=post)
            uploaded = post_get.uploaded_file_set.all()
            list = []
            for i in uploaded:
                list.append(i.file)
            count = 0
            form = PostUpdateform(request.POST,instance=post_get)
            if form.is_valid():
                form.save()
                if request.FILES.getlist('file'):
                    if len(request.FILES.getlist('file')) > len(list):
                        for get_file,files in itertools.zip_longest(request.FILES.getlist('file'),list):
                            count += 1
                            if count > len(list):
                                Uploaded_File.objects.create(post=post_get,file=get_file,writer=post_get.writer)
                            else:
                                Uploaded_File.objects.filter(post= post_get,file = files).update(file = get_file)
                    elif len(request.FILES.getlist('file')) == len(list):
                        for get_file,files in itertools.zip_longest(request.FILES.getlist('file'),list):
                            Uploaded_File.objects.filter(post= post_get,file = files).update(file = get_file)
                    elif len(request.FILES.getlist('file')) < len(list):
                        for get_file,files in itertools.zip_longest(request.FILES.getlist('file'),list):
                            count +=1
                            if count > len(request.FILES.getlist('file')):
                                Uploaded_File.objects.filter(post= post_get,file =files).delete()
                            else:
                                Uploaded_File.objects.filter(post= post_get,file = files).update(file = get_file)
                return HttpResponseRedirect(reverse('web:post',args=(post,)))
            else:
                try:
                    form = PostUpdateform()
                    Bt = BoardTable.objects.all()
                    return render(request,'web/updatepost.html',{'form':form,'pk':post,'updateposterror':"글 없음",'boardtable':Bt})
                except:
                    return HttpResponse('올바르지 않습니다.')
        except:
            return HttpResponse('올바르지않습니다.')


#게시글 삭제 클래스 뷰
class DeletePostView(View):
    def get(self,request,post,*args,**kwargs):
        posts = get_object_or_404(Post,pk=post)
        posts.delete()
        return HttpResponseRedirect(reverse('web:website'))

# 상위게시판 생성 클래스 뷰
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
                form =Bcreateform(initial={'supervisor':request.session['logined'],'grade':request.session['logined']})
                return render(request,'web/createboardtable.html',{'Bform':form,'Btsuccess':"상위게시판생성완료"})

#하위 게시판 생성 클래스 뷰
class BcreateView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined_special'):
            form = Bcreateform(initial={'supervisor':request.session['logined'],'grade':request.session['logined']})
            return render(request,'web/createboardtable.html',{'Bform':form})


    def post(self,request,*args,**kwargs):
        form = Bcreateform(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            form =Bcreateform(initial={'supervisor':request.session['logined'],'grade':request.session['logined']})
            return render(request,'web/createboardtable.html',{'Bform':form,'Bsuccess':"하위게시판생성완료"})


# 게시글 생성 클래스 뷰
class BpCreateView(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('logined_special'):
            form = PostCreateform(initial={'writer':request.session['logined']})
            return render(request,'web/createboardtable.html',{'Pform':form})
        else:
            raise PermissionDenied

    def post(self,request,*args,**kwargs):
        form = PostCreateform(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.professor = 1
            form.save()
            form = PostCreateform(initial={'writer':request.session['logined']})
            return render(request,'web/createboardtable.html',{'Pform':form,'Psuccess':"게시글 작성완료"})


# 추천 클래스 뷰
class likeView(View):
    def get(self,request,post,*args,**kwargs):
        try:
            posts = get_object_or_404(Post,pk=post)
            student = Student.objects.get(id = request.session['logined_student_id'])
            email = student.email
            check_like_post = student.like_post.filter(id = post)
            files = posts.uploaded_file_set.all()
            reply = posts.reply_set.all()
            Bt = BoardTable.objects.all()
            form = Replyform()
            if check_like_post.exists():
                student.like_post.remove(posts)
                posts.like_number -= 1
                posts.save()
            else:
                student.like_post.add(posts)
                posts.like_number += 1
                posts.save()

            return render(request,'web/post.html',{'email':email,'post':posts,'pk':post,'success':" ",'files':files,'reply':reply,'boardtable':Bt,'replyform':form,})
        except:
            try:
                posts = get_object_or_404(Post,pk=post)
                professor = Professor.objects.get(id = request.session['logined_professor_id'])
                email = professor.email
                check_like_post = professor.like_post.filter(id = post)
                files = posts.uploaded_file_set.all()
                reply = posts.reply_set.all()
                Bt = BoardTable.objects.all()
                form = Replyform()
                if check_like_post.exists():
                    professor.like_post.remove(posts)
                    posts.like_number -=1
                    posts.save()
                else:
                    professor.like_post.add(posts)
                    posts.like_number += 1
                    posts.save()

                return render(request,'web/post.html',{'email':email,'post':posts,'pk':post,'success':" ",'files':files,'reply':reply,'boardtable':Bt,'replyform':form,})
            except:
                try:
                    posts = get_object_or_404(Post,pk=post)
                    files = posts.uploaded_file_set.all()
                    reply = posts.reply_set.all()
                    Bt = BoardTable.objects.all()
                    form = Replyform()
                    return render(request,'web/post.html',{'post':posts,'pk':post,'error':" ",'files':files,'reply':reply,'boardtable':Bt,'replyform':form,})
                except:
                    return HttpResponse('올바르지 않습니다.')


class LikeBoardView(View):
    def get(self,request,boardtable,board,*args,**kwargs):
        try:
            boardtables =get_object_or_404(BoardTable,pk=boardtable)
            boards = boardtables.board_set.all()
            get_board = get_object_or_404(Board,pk=board)
            name = get_board.board_name
            post = get_board.post_set.filter(like_number__gt = 0)
            Bt = BoardTable.objects.all()
            if post:
                return render(request,'web/board.html',{'post':post,'board':boards,'pk':boardtable,'ak':board,'boardtable':Bt,'name':name,'likeboard':"인기글"})
            else:
                return render(request,'web/board.html',{'post':post,'board':boards,'pk':boardtable,'ak':board,'boardtable':Bt,'name':name,'likeboard':"인기글",'likeboarderror':"인기글 존재x"})
        except:
            return HttpResponse('올바르지않습니다.')


# class MyPageView(View):
#     def get(self,request,*args,**kwargs):
#         if request.session.get('logined_student_id'):
#             student = Student.objects.get(id = request.session['logined_student_id'])
#             return render(request,'web/mypage.html',{'student':student})
#         elif request.session.get('logined_professor_id'):
#             professor = Professor.objects.get(id = request.session['logined_professor_id'])
#             return render(request,'web/mypage.html',{'professor':professor})
