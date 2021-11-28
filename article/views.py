import json
import os
import time

from BarProject import settings
from users.models import User, User_info
from .models import Article, Bar, Reply
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.

# 处理提交的文章

def writeArticle(request):
    if request.method == 'GET':
        return HttpResponse('获取数据111')
    if request.method == 'POST':
        # 准备返回的数据
        data = {'code': 200}
        # 获取当前用户提交的文章
        title = json.loads(request.body)['title']
        content = json.loads(request.body)['text']
        user_id = request.session.get('user_id')
        bar_id = json.loads(request.body)['bar_id']
        # 标题不能少于5个字符 和不能多于100个字符
        if len(title) < 5 or len(title) > 100:
            data['message'] = '标题不能少于5个字符或者大于100个字符'
            data['code'] = 400
            return HttpResponse(json.dumps(data))
        # 文章内容不能为空
        if not content:
            data['message'] = '文章内容不能为空'
            data['code'] = 400
            return HttpResponse(json.dumps(data))
        # 保存文章到表格里面
        Article.objects.create(user_id=user_id, title=title, content=content, bar_id=bar_id)
        data['message'] = '文章提交成功，待审核中'
        # 提交文章成功后用户涨经验+2exp
        user_info = User_info.objects.filter(user_id=user_id)[0]
        user_info.exp += 2
        user_info.save()
        return HttpResponse(json.dumps(data))


# 获取文章
def getArt(request):
    if request.method == 'GET':
        # 返回的数据
        data = {'code': 200}
        # # 获取当前用户资料的信息
        # user = User.objects.filter(username=request.session.get('username'))[0]
        # # 获取用户的文章
        # user_art = Article.objects.filter(user=user)
        # 对数据进行排序
        sort = request.GET.get('sort', '')
        art = Article.objects.filter(is_active=True)
        if sort == 'newest':
            art = art.order_by('-updated_time')
        article_list = []
        for t in art:
            # print(len(Reply.objects.filter(article_id=t.id, is_active=True)))
            t.id = {'id': t.id,
                    'title': t.title,
                    'content': t.content,
                    'user_id': t.user_id,
                    'bar_id': t.bar_id,
                    'created_time': str(t.created_time),
                    # 获取回帖数
                    'reply_num': len(Reply.objects.filter(article_id=t.id, is_active=True))
                    }

            article_list.append(t.id)
        data['article_list'] = article_list
        data['message'] = '获取文章成功'
        return HttpResponse(json.dumps(data))
    elif request.method == 'POST':
        return HttpResponse('POST请求')


# 获取单个文章内容
def getOneArticle(request):
    if request.method == 'GET':
        # 设置返回数据
        data = {'code': 200}
        # 获取当前用户提交的数据
        id = request.GET.get('article_id')
        # 获取当前文章并返回
        article = Article.objects.filter(id=id)[0]
        data['title'] = article.title
        data['content'] = article.content
        data['user_id'] = article.user_id
        data['up_time'] = str(article.updated_time)[0:19]
        # 获取用户个人信息
        userInfo = User_info.objects.filter(user_id=article.user_id)[0]
        data['nick_name'] = userInfo.nick_name
        data['portrait'] = str(userInfo.portrait)
        data['exp'] = userInfo.exp
        data['message'] = '获取成功'
        return HttpResponse(json.dumps(data))
    elif request.method == 'POST':
        # 设置返回数据
        data = {'code': 200}
        data['message'] = '请求成功'
        return HttpResponse(json.dumps(data))


# 创建主题
def createBar(request):
    if request.method == 'GET':
        # 返回的资料
        data = {'code': 200}
        # 检查当前用户是否存在
        user = User.objects.filter(username=request.session.get('username'))[0]
        if not user:
            data['code'] = 400
            data['message'] = '用户不存在，请重新登录'
            return HttpResponse(json.dumps(data))
        # 获取当前用户提交的资料
        getData = json.loads(request.GET.get('data'))
        username = getData['username']
        bar_name = getData['bar_name']
        int = getData['int']
        id_card = getData['id_card']
        # 检查用户名和当前登录的用户是否相同
        if user.username != username:
            data['code'] = 400
            data['message'] = '当前用户不匹配'
            return HttpResponse(json.dumps(data))
        # 检查主题名 和身份证不能为空
        if not bar_name and not id_card:
            data['code'] = 400
            data['message'] = '主题名和身份证不能为空'
            return HttpResponse(json.dumps(data))
        # 检查当前主题名是否重复
        if Bar.objects.filter(bar_name=bar_name):
            data['code'] = 400
            data['message'] = '主题名已存在'
            return HttpResponse(json.dumps(data))
        # 如需添加审核在此处填写
        # 创建主题吧
        Bar.objects.create(bar_name=bar_name, user=user, int=int, id_card=id_card)
        data['message'] = '申请已提交，待审核中'
        return HttpResponse(json.dumps(data))

    elif request.method == 'POST':
        return HttpResponse('请求成功')


# 查询主题吧
def search_bar(request):
    if request.method == 'GET':
        # 获取返回搜索范围
        search_type = request.GET.get('search_type', '')
        bar_id = request.GET.get('bar_id', '')
        data = {'code': 200}
        data['message'] = '搜索成功'
        # 获取用户要搜索的内容
        searchData = request.GET.get('seachData')
        # 判断下内容是否为空
        if not searchData:
            data['code'] = 400
            data['message'] = '搜索框不能为空哦'
            return HttpResponse(json.dumps(data))
        # 搜索用户请求的内容
        barData = Bar.objects.filter(bar_name__contains=searchData)
        # 返回主题名和id
        bar_names = []
        for b in barData:
            b.id = {'bar_name': b.bar_name, 'id': b.id, 'created_time': str(b.created_time), 'int': b.int}
            bar_names.append(b.id)
        data['bar_data'] = bar_names
        # 搜索帖子内容
        art_data = []
        articleData = Article.objects.filter(title__contains=searchData, is_active=True)
        if search_type == 'bar':
            articleData = Article.objects.filter(title__contains=searchData, is_active=True, bar_id=bar_id)
        for a in articleData:
            a.id = {'title': a.title, 'content': a.content, 'id': a.id, 'updated_time': str(a.updated_time)}
            art_data.append(a.id)
        data['art_data'] = art_data
        print(data)
        return HttpResponse(json.dumps(data))


# 获取bar的文章
def getBarArt(request):
    if request.method == 'GET':
        # 返回数据
        data = {'code': 200}
        # 获取用户提交的bar_id
        bar_id = request.GET.get('bar_id')
        # 获取吧的文章和信息
        barData = Bar.objects.filter(id=bar_id, is_active=True)[0]
        # 获取bar的文章
        barArt = Article.objects.filter(bar=barData, is_active=True).order_by('-updated_time')
        art_data = []
        # 处理保存下文章数据
        for a in barArt:
            a.id = {'title': a.title, 'content': a.content, 'id': a.id, 'create_time': str(a.created_time),
                    'updated_time': str(a.updated_time)}
            art_data.append(a.id)
        data['art_data'] = art_data
        # 处理保存下主题信息
        bar_data = {'id': barData.id, 'bar_name': barData.bar_name, 'portrait': str(barData.portrait),
                    'int': barData.int,
                    'created_time': str(barData.created_time),
                    'barUserName': User.objects.filter(id=barData.user_id, is_active=True)[0].username
                    }
        data['bar_data'] = bar_data
        data['message'] = '获取成功'
        return HttpResponse(json.dumps(data))


# 写回帖
def writeReply(request):
    if request.method == 'POST':
        # 返回数据
        data = {'code': 200}
        # 获取回帖
        art_id = json.loads(request.body)['art_id']
        replyText = json.loads(request.body)['replyText']
        # 回帖内容如果为空，报错
        if not replyText:
            data['code'] = 400
            data['message'] = '回帖内容不能为空'
            return HttpResponse(json.dumps(data))
        # 获得当前文章
        art = Article.objects.filter(id=art_id, is_active=True)[0]
        # 获得用户
        user = User.objects.filter(username=request.session.get('username'), is_active=True)[0]
        # 创建回帖
        Reply.objects.create(user=user, article=art, content=replyText)
        data['message'] = '回帖成功，待审核通过后查看'
        return HttpResponse(json.dumps(data))


# 获取回帖
def getReply(request):
    if request.method == 'GET':
        # 返回数据
        data = {'code': 200}
        # 获取用户提交的art_id
        art_id = request.GET.get('art_id')
        # 获取文章的回帖
        reply = Reply.objects.filter(article_id=art_id)
        replyData = []
        for r in reply:
            r.id = {
                'id': r.id,
                'user_id': r.user_id,
                'reply_text': r.content,
                # 获取用户的头像和名字
                'username': User.objects.filter(id=r.user_id)[0].username,
                'nick_name': User_info.objects.filter(user_id=r.user_id)[0].nick_name,
                'portrait': str(User_info.objects.filter(user_id=r.user_id)[0].portrait),
                'updated_time': str(r.updated_time)}
            replyData.append(r.id)
        print(replyData)
        data['replyData'] = replyData
        data['message'] = '获取回帖成功'
        return HttpResponse(json.dumps(data))


def getBarData(request):
    if request.method == 'GET':
        # 返回数据
        data = {'code': 200}
        # 获取用户提交的bar_id
        bar_id = request.GET.get('bar_id', '')
        if not bar_id:
            data['code'] = 400
            data['message'] = '主题不存在，请进入主题后重试'
            return HttpResponse(json.dumps(data))
        # 查询主题的资料
        bar = Bar.objects.filter(id=bar_id, is_active=True)[0]
        barData = {
            'id': bar.id,
            'bar_name': bar.bar_name,
            'portrait': str(bar.portrait),
            'int': bar.int,
            'id_card': bar.id_card,
            'user': User.objects.filter(id=bar.user_id, is_active=True)[0].username
        }
        # 把资料传回去
        data['barData'] = barData
        data['message'] = '获取主题数据成功'
        return HttpResponse(json.dumps(data))


# 设置bar数据
def setBar(request):
    if request.method == 'GET':
        # 返回的数据
        data = {'code': 200}
        # 获取提交的数据
        bar_id = request.GET.get('bar_id')
        int = request.GET.get('int')
        print(int)
        # 保存数据
        bar = Bar.objects.filter(id=bar_id, is_active=True)[0]
        bar.int = int
        bar.save()
        data['message'] = '保存成功'
        return HttpResponse(json.dumps(data))


# 上传头像
def postBarPortrait(request):
    if request.method == 'POST':
        # 返回的数据
        data = {'code': 200}
        # 获取图片
        bar_id = request.POST.get('bar_id')
        portrait = request.FILES.get('file')
        file_name = portrait.name
        # 编辑保存的路径
        path = os.path.join(settings.MEDIA_ROOT,
                            'img/bar_portrait/' + time.strftime("%Y-%m-%d", time.localtime()) + '-' + file_name)
        # 写入本地储存
        with open(path, 'wb')as f:
            data_file = portrait.file.read()
            f.write(data_file)
        data['message'] = '保存数据成功'
        # 保存到当前bar表
        bar = Bar.objects.filter(id=bar_id, is_active=True)[0]
        bar.portrait = portrait
        bar.save()
        return HttpResponse(json.dumps(data))
