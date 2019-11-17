from django.db import models

# Create your models here.



class Student(models.Model):
    name = models.CharField(max_length=20,verbose_name="이름")
    email = models.CharField(max_length=30,verbose_name="아이디")
    student_number = models.CharField(max_length=10,verbose_name="학번")
    password = models.CharField(max_length=20,verbose_name="비밀번호")
    grade = models.CharField(max_length=10,verbose_name="학년")
    tutor = models.CharField(max_length=10,verbose_name="지도교수")


    def __str__(self):
        return self.name


class Professor(models.Model):
    name = models.CharField(max_length=20,verbose_name="이름")
    email = models.CharField(max_length=30,verbose_name="아이디")
    professor_number = models.CharField(max_length=10,verbose_name="직원번호")
    password = models.CharField(max_length=20,verbose_name="비밀번호")

    def __str__(self):
        return self.name


class Table(models.Model):
    Type = models.CharField(max_length=20, verbose_name="게시판 종류")

class Grade_Table(models.Model):
    grade = models.CharField(max_length=10, verbose_name="학년")
    title = models.CharField(max_length=10,verbose_name="제목")
    description = models.TextField(verbose_name="내용")
    writer = models.CharField(max_length=10,verbose_name="작성자")
    date = models.DateField(auto_now=True,verbose_name="작성일")

    def __str__(self):
        return self.title

    


class Professor_Table(models.Model):
    professor_name = models.CharField(max_length=10, verbose_name="지도교수")
    title = models.CharField(max_length=10,verbose_name="제목")
    description = models.TextField(verbose_name="내용")
    writer = models.CharField(max_length=10,verbose_name="작성자")
    date = models.DateField(auto_now=True,verbose_name="작성일")

    
    def __str__(self):
        return self.title




class Course(models.Model):
    name = models.CharField(max_length=10,verbose_name="강의명")
    professor = models.CharField(max_length=10,verbose_name="교수명")

    def __str__(self):
        return self.name


class Course_Table(models.Model):
    course_name = models.ForeignKey(Course, on_delete= models.CASCADE)
    title = models.CharField(max_length=10,verbose_name="제목")
    description = models.TextField(verbose_name="내용")
    writer = models.CharField(max_length=10,verbose_name="작성자")
    date = models.DateField(auto_now=True,verbose_name="작성일")

    
    def __str__(self):
        return self.title