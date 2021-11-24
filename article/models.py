from django.db import models
#  引入 ueditor 富文本
from DjangoUeditor.models import UEditorField
# Create your models here.
from users.models import User


# 主题表
class Bar(models.Model):
    id = models.AutoField('ID', primary_key=True)
    bar_name = models.CharField('论坛名', max_length=10, unique=True, default='')
    portrait = models.FileField('主题头像', upload_to='img/bar_portrait/', default='')
    int = models.CharField('简介', max_length=38, default='')
    id_card = models.CharField('身份证', max_length=18, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField('是否活跃', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'bar'


# 文章表
class Article(models.Model):
    id = models.AutoField('ID', primary_key=True)
    title = models.CharField('标题', max_length=100, default='')
    content = UEditorField(u'内容	', width=600, height=300, toolbars="full",
                           imagePath="images/images/%(basename)s_%(datetime)s.%(extname)s",
                           filePath="files/%(basename)s_%(datetime)s.%(extname)s",
                           upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, event_handler='', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE, default=1)
    is_active = models.BooleanField('是否活跃', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'Article'


# 回帖表
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = UEditorField(u'内容	', width=600, height=300, toolbars="full",
                           imagePath="images/images/%(basename)s_%(datetime)s.%(extname)s",
                           filePath="files/%(basename)s_%(datetime)s.%(extname)s",
                           upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, event_handler='', blank=True)
    is_active = models.BooleanField('是否活跃', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'Reply'
