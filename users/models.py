from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField('ID', primary_key=True)
    username = models.CharField('用户名', max_length=22, default='')
    password = models.CharField('密码', max_length=78, default='')
    email = models.EmailField('邮箱')
    sex = models.CharField('性别', max_length=2, default='')
    phone = models.CharField('手机号', max_length=11, default='')
    is_active = models.BooleanField('是否活跃', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user'


# 创建用户详细资料表
class User_info(models.Model):
    id = models.AutoField('ID', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portrait = models.FileField('头像', upload_to='img/head_portrait/')
    nick_name = models.CharField('昵称', max_length=10, default='', unique=True)
    age = models.IntegerField('年龄', default=0)
    sex = models.CharField('性别', max_length=1, default='无')
    id_card = models.CharField('身份证', max_length=18, default='', unique=True)
    exp = models.IntegerField('经验', default=0)
    bar_coin = models.IntegerField('趣味币', default=0)
    is_active = models.BooleanField('是否活跃', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_info'
