# Generated by Django 2.2.6 on 2019-12-12 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='메세지')),
                ('writer', models.CharField(max_length=10, verbose_name='작성자')),
                ('writer_email', models.EmailField(max_length=30, verbose_name='작성자 아이디')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='작성일자')),
                ('attn_email', models.EmailField(max_length=30, verbose_name='수신자 아이디')),
            ],
        ),
    ]
