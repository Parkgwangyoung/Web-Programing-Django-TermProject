from django.db import models

# Create your models here.

class BoardTable(models.Model):
    board_type = models.CharField(max_length=20, verbose_name="상위 게시판이름")

    def __str__(self):
        return self.board_type

class Board(models.Model):
    board_type = models.ForeignKey(BoardTable,on_delete=models.CASCADE)
    board_name = models.CharField(max_length=20,verbose_name="게시판 이름")
    
    def __str__(self):
        return self.board_name


class Post(models.Model):
    board_name = models.ForeignKey(Board,on_delete=models.CASCADE)
    title = models.CharField(max_length=20,verbose_name="제목")
    description = models.TextField(verbose_name="글 내용")
    writer = models.CharField(max_length=10,verbose_name="작성자")
    date = models.DateField(auto_now=True,verbose_name="작성일")

    def __str__(self):
        return self.title


