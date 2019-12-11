from django.db import models

class Mail(models.Model):
    title = models.CharField(max_length=10, verbose_name="메일 제목")
    description = models.TextField(verbose_name="메일 내용")
    writer = models.CharField(max_length=10,verbose_name="메일 작성자")
    writer_email = models.EmailField(max_length=30,verbose_name="작성자 아이디")
    attn_email = models.EmailField(max_length=30,verbose_name="받는사람 아이디")
    date = models.DateTimeField(auto_now=True, verbose_name="작성일자")


    def __str__(self):
        return self.writer

