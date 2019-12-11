from django.shortcuts import render
from django.views import View
from chatting.models import Chat
from chatting.forms import chatform 
from django.http import HttpResponse,HttpResponseRedirect
from login.models import Student,Professor
from django.urls import reverse
import itertools
# Create your views here.



class chatView(View):
    def get(self,request,*args,**kwargs):
        chatting = Chat.objects.all().order_by('-date')[:5]    
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
        return render(request,'chatting/room.html',{'chat':chat,'form':form})

    def post(self,request,*args,**kwargs):
        student = Student.objects.get(id = request.session['logined_student_id'])
        form = chatform(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.writer = student.name
            chat.writer_email = student.email
            chat.save()
            return HttpResponseRedirect(reverse('chatting:chat'))


