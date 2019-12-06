from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=20,verbose_name="이름")
    email = models.EmailField(max_length=30,verbose_name="아이디")
    student_number = models.CharField(max_length=10,verbose_name="학번")
    password = models.CharField(max_length=20,verbose_name="비밀번호")
    grade = models.CharField(max_length=10,verbose_name="학년")
    tutor = models.CharField(max_length=10,verbose_name="지도교수")
    file_post = models.ManyToManyField("web.Post",blank=True, related_name='학생파일업로드',verbose_name="파일명")
    like_post = models.ManyToManyField("web.Post" ,blank=True,  related_name='학생추천수',verbose_name="


    def __str__(self):
        return self.name

class Professor(models.Model):
    name = models.CharField(max_length=20,verbose_name="이름")
    email = models.EmailField(max_length=30,verbose_name="아이디")
    professor_number = models.CharField(max_length=10,verbose_name="직원번호")
    password = models.CharField(max_length=20,verbose_name="비밀번호")
    like_post = models.ManyToManyField("web.Post", blank=True,related_name='교수추천수',verbose_name="추천수")
    file_post = models.ManyToManyField("web.Post",blank=True, related_name='교수파일업로드',verbose_name="파일명")

    def __str__(self):
        return self.name
