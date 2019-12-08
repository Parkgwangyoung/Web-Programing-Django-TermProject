from django.db import models

# Create your models here.

class BoardTable(models.Model):
    board_type = models.CharField(max_length=20, verbose_name="상위 게시판이름")

    def __str__(self):
        return self.board_type

class Board(models.Model):
    board_type = models.ForeignKey(BoardTable,on_delete=models.CASCADE,verbose_name="하위 게시판이름")
    board_name = models.CharField(max_length=20,verbose_name="게시판 이름")
    supervisor = models.CharField(max_length=10, verbose_name="지도 교수")
    grade = models.CharField(max_length=10,verbose_name="학년")
    
    def __str__(self):
        return self.board_name


class Post(models.Model):
    board_name = models.ForeignKey(Board,on_delete=models.CASCADE,verbose_name="게시판 이름")
    student = models.ForeignKey("login.Student",null=True,on_delete=models.CASCADE,verbose_name="학생")
    professor = models.ForeignKey("login.Professor",null=True,on_delete=models.CASCADE,verbose_name="교수")
    title = models.CharField(max_length=20,verbose_name="제목")
    description = models.TextField(verbose_name="글 내용")
    writer = models.CharField(max_length=10,verbose_name="작성자")
    writer_email = models.EmailField(max_length=30,verbose_name="작성자 아이디")
    date = models.DateField(auto_now=True,verbose_name="작성일") 
    like_number  = models.PositiveIntegerField(default=0,verbose_name="추천수")

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

class Uploaded_File(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, verbose_name="글 제목")
    file = models.FileField(upload_to='',verbose_name="파일명",blank=True)
    writer = models.CharField(max_length=10, verbose_name="작성자")

    # def __str__(self):
    #     return self.writer

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name = "글 제목")
    reply = models.TextField(verbose_name="댓글 내용")
    writer = models.CharField(max_length=10, verbose_name="작성자")

    def __str__(self):
        return self.writer



