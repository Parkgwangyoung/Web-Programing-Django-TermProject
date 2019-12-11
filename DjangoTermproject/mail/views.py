from django.shortcuts import render,get_object_or_404
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from mail.models import Mail
from mail.forms import CreateMailform
from login.models import Student,Professor
from django.urls import reverse


class MailIndexView(View):
    def get(self,request,*args,**kwargs):
        try:
            if request.session.get('logined_student_id'):
                student = Student.objects.get(id = request.session['logined_student_id'])
                email = student.email
                mail_list = Mail.objects.filter(attn_email = email)
                return render(request,'mail/mailindex.html',{'mail_list':mail_list})
            elif request.session.get('logined_professor_id'):
                professor = Professor.objects.get(id = request.session['logined_professor_id'])
                email = professor.email
                mail_list = Mail.objects.filter(attn_email = email)
                return render(request,'mail/mailindex.html',{'mail_list':mail_list})
        except:
            return HttpResponse('어드민은 메일을 보낼 수 없습니다.')


class MailDetailView(View):
    def get(self,request,mail_id,*args,**kwargs):
        mail_get = get_object_or_404(Mail , pk = mail_id)
        return render(request,'mail/mail.html',{'mail':mail_get})



class CreateMailView(View):
    def get(self,request,*args,**kwargs):
        form = CreateMailform()
        return render(request,'mail/createmail.html',{'form':form})

    def post(self,request,*args,**kwargs):
        try:
            if request.session.get('logined_student_id'):
                student = Student.objects.get(id = request.session['logined_student_id'])
                email = student.email
                form = CreateMailform(request.POST)
                if form.is_valid():
                    attn_email = form.cleaned_data['attn_email']
                    try:
                        Student.objects.get(email = attn_email)
                        mail = form.save(commit=False)
                        mail.writer = request.session['logined']
                        mail.writer_email = email
                        mail.save()
                        return HttpResponseRedirect(reverse('mail:mailindex'))
                    except:
                        try:
                            Professor.objects.get(email = attn_email)
                            mail = form.save(commit=False)
                            mail.writer = request.session['logined']
                            mail.writer_email = email
                            mail.save()
                            return HttpResponseRedirect(reverse('mail:mailindex'))
                        except:
                            return HttpResponse('올바르지 않습니다.')
            elif request.session.get('logined_professor_id'):
                professor = Professor.objects.get(id = request.session['logined_professor_id'])
                email = professor.email
                form = CreateMailform(request.POST)
                if form.is_valid():
                    attn_email = form.cleaned_data['attn_email']
                    try:
                        Student.objects.get(email = attn_email)
                        mail = form.save(commit=False)
                        mail.writer = request.session['logined']
                        mail.writer_email = email
                        mail.save()
                        return HttpResponseRedirect(reverse('mail:mailindex'))
                    except:
                        try:
                            Professor.objects.get(email = attn_email)
                            mail = form.save(commit=False)
                            mail.writer = request.session['logined']
                            mail.writer_email = email
                            mail.save()
                            return HttpResponseRedirect(reverse('mail:mailindex'))
                        except:
                            return HttpResponse('올바르지 않습니다.')
            else:       
                return HttpResponse('관리자는 메일을 보낼수없습니다.')
        except:
            return HttpResponse('올바르지않습니다.')
                    
                    