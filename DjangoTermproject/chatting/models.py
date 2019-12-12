from django.db import models

# Create your models here.


class Chat(models.Model):
    text = models.TextField(verbose_name="메세지")
    writer = models.CharField(max_length=10,verbose_name="작성자")
    writer_email = models.EmailField(max_length=30,verbose_name="작성자 아이디")
    date = models.DateTimeField(auto_now=True,verbose_name="작성일자")
    attn_email = models.EmailField(max_length=30,verbose_name="수신자 아이디")
    
    def __str__(self):
        return self.text