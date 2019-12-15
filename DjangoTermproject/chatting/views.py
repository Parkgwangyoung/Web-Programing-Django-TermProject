from django.shortcuts import render
from django.views import View
from chatting.models import Chat
from chatting.forms import chatform 
from django.http import HttpResponse,HttpResponseRedirect
from login.models import Student,Professor
from web.models import BoardTable, Board
from django.urls import reverse
from django.db.models import Q

# Create your views here.



class indexView(View):
    def get(self,request,select,*args,**kwargs):
        try:
            Bt = BoardTable.objects.all()
            if select == 1:
                if request.session.get('logined_student_id'):
                    student_list = Student.objects.all().exclude(id = request.session['logined_student_id']).exclude(id = 1)
                    return render(request,'chatting/index.html',{'student_list':student_list,'boardtable':Bt})
                elif request.session.get('logined_professor_id'):
                    student_list = Student.objects.all().exclude(id = 1)
                    return render(request,'chatting/index.html',{'student_list':student_list,'boardtable':Bt})
                else:
                    return HttpResponse('관리자는 채팅할 수 없습니다.')
            else:
                if request.session.get('logined_student_id'):
                    professor_list = Professor.objects.all()
                    return render(request,'chatting/index.html',{'professor_list':professor_list,'boardtable':Bt})
                elif request.session.get('logined_professor_id'):
                    professor_list = Professor.objects.all().exclude(id =request.session['logined_professor_id'])
                    return render(request,'chatting/index.html',{'professor_list':professor_list,'boardtable':Bt})
                else:
                    return HttpResponse('관리자는 채팅할 수 없습니다.')
        except:
            return HttpResponse('올바르지 않습니다.')
class chatView(View):
    def get(self,request,select,member,*args,**kwargs):
        if select == 1:
            if request.session.get('logined_student_id'):
                try:
                    Bt = BoardTable.objects.all()
                    attn = Student.objects.get(id = member)
                    student= Student.objects.get(id = request.session['logined_student_id'])
                    chatting = Chat.objects.all().filter(Q(writer_email = student.email, attn_email = attn.email) | Q(writer_email = attn.email , attn_email = student.email)).order_by('-date')[:5]  
                    writers = []
                    texts=[]
                    dates=[]
                    for i in chatting:
                        writers.append(i.writer)
                        texts.append(i.text)
                        dates.append(i.date)
                    writers.reverse()      
                    texts.reverse()
                    dates.reverse()
                    chat = zip(texts,writers,dates)        
                    form = chatform()
                    return render(request,'chatting/room.html',{'chat':chat,'form':form,'student_id':member,'boardtable':Bt})
                except:
                    return HttpResponse('s')
            elif request.session.get('logined_professor_id'):
                try:
                    Bt = BoardTable.objects.all()
                    attn = Student.objects.get(id = member)
                    professor = Professor.objects.get(id = request.session['logined_professor_id'])
                    chatting = Chat.objects.all().filter(Q(writer_email = professor.email, attn_email = attn.email) | Q(writer_email = attn.email , attn_email = professor.email)).order_by('-date')[:5]  
                    writers = []
                    texts=[]
                    dates=[]
                    for i in chatting:
                        writers.append(i.writer)
                        texts.append(i.text)
                        dates.append(i.date)
                    writers.reverse()      
                    texts.reverse()
                    dates.reverse()
                    chat = zip(texts,writers,dates)        
                    form = chatform()
                    return render(request,'chatting/room.html',{'chat':chat,'form':form,'student_id':member,'boardtable':Bt})
                except:
                    return HttpResponse('s')
            else:
                return HttpResponse('관리자는 채팅할 수 없습니다.')
        else:
            if request.session.get('logined_student_id'):
                try:
                    Bt = BoardTable.objects.all()
                    attn = Professor.objects.get(id = member)
                    student= Student.objects.get(id = request.session['logined_student_id'])
                    chatting = Chat.objects.all().filter(Q(writer_email = student.email, attn_email = attn.email) | Q(writer_email = attn.email , attn_email = student.email)).order_by('-date')[:5]  
                    writers = []
                    texts=[]
                    dates=[]
                    for i in chatting:
                        writers.append(i.writer)
                        texts.append(i.text)
                        dates.append(i.date)
                    writers.reverse()      
                    texts.reverse()
                    dates.reverse()
                    chat = zip(texts,writers,dates)        
                    form = chatform()
                    return render(request,'chatting/room.html',{'chat':chat,'form':form,'professor_id':member,'boardtable':Bt})
                except:
                    return HttpResponse('s')
            elif request.session.get('logined_professor_id'):
                try:
                    Bt = BoardTable.objects.all()
                    attn = Professor.objects.get(id = member)
                    professor = Professor.objects.get(id = request.session['logined_professor_id'])
                    chatting = Chat.objects.all().filter(Q(writer_email = professor.email, attn_email = attn.email) | Q(writer_email = attn.email , attn_email = professor.email)).order_by('-date')[:5]  
                    writers = []
                    texts=[]
                    dates=[]
                    for i in chatting:
                        writers.append(i.writer)
                        texts.append(i.text)
                        dates.append(i.date)
                    writers.reverse()      
                    texts.reverse()
                    dates.reverse()
                    chat = zip(texts,writers,dates)        
                    form = chatform()
                    return render(request,'chatting/room.html',{'chat':chat,'form':form,'professor_id':member,'boardtable':Bt})
                except:
                    return HttpResponse('s')
            else:
                return HttpResponse('관리자는 채팅할 수 없습니다.')

    def post(self,request,select,member,*args,**kwargs):
        if select == 1:
            if request.session.get('logined_student_id'):
                try:
                    attn = Student.objects.get(id = member)
                    student = Student.objects.get(id = request.session['logined_student_id'])
                    form = chatform(request.POST)
                    if form.is_valid():
                        chat = form.save(commit=False)
                        chat.writer = student.name
                        chat.writer_email = student.email
                        chat.attn_email = attn.email
                        chat.save()
                        return HttpResponseRedirect(reverse('chatting:chat',args=(select,member,)))
                except:
                    return HttpResponse('올바르지 않습니다')
            else:
                try:
                    attn = Student.objects.get(id = member)
                    professor = Professor.objects.get(id = request.session['logined_professor_id'])
                    form = chatform(request.POST)
                    if form.is_valid():
                        chat = form.save(commit=False)
                        chat.writer = professor.name
                        chat.writer_email = professor.email
                        chat.attn_email = attn.email
                        chat.save()
                        return HttpResponseRedirect(reverse('chatting:chat',args=(select,member,)))
                except:
                    return HttpResponse('올바르지 않습니다.')
        
        else:
            if request.session.get('logined_student_id'):
                try:
                    attn = Professor.objects.get(id = member)
                    student = Student.objects.get(id = request.session['logined_student_id'])
                    form = chatform(request.POST)
                    if form.is_valid():
                        chat = form.save(commit=False)
                        chat.writer = student.name
                        chat.writer_email = student.email
                        chat.attn_email = attn.email
                        chat.save()
                        return HttpResponseRedirect(reverse('chatting:chat',args=(select,member,)))
                except:
                    return HttpResponse('올바르지 않습니다')
            else:
                try:
                    attn = Professor.objects.get(id = member)
                    professor = Professor.objects.get(id = request.session['logined_professor_id'])
                    form = chatform(request.POST)
                    if form.is_valid():
                        chat = form.save(commit=False)
                        chat.writer = professor.name
                        chat.writer_email = professor.email
                        chat.attn_email = attn.email
                        chat.save()
                        return HttpResponseRedirect(reverse('chatting:chat',args=(select,member,)))      
                except:
                    return HttpResponse('올바르지 않습니다.')
                



