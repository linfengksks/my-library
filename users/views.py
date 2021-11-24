import os
import time

from django.shortcuts import render
from django.http import HttpResponse, response
from django.middleware.csrf import get_token
import json

from BarProject import settings
from .models import User, User_info
# 一组加密算法
from django.contrib.auth import hashers
from django.core import serializers


# Create your views here.
# 登录页面
def login(request):
    # 返回token值给前端
    if request.method == 'GET':
        # 获取csrf_token的值
        csrf_token = get_token(request)
        return HttpResponse(csrf_token)
    if request.method == 'POST':
        # 得到json字符串 通过json.loads转换为字典，然后去其中的数据
        post_data = json.loads(request.body)['data']
        # 接收收到的请求
        username = post_data['username']
        # 创建返回的数据对象
        data = {'code': 200}
        # 判断当前用户是否存在
        if User.objects.filter(username=username):
            password_hash = User.objects.filter(username=username)[0].password
        else:
            data['code'] = 400
            return HttpResponse(json.dumps(data))
        # password = hashers.check_password(data['password'], password_hash)
        # 判断帐号密码是否正确
        # if password:
        #     # 生产加密盐用户
        #     username_has = hashers.make_password(username)
        #     data = {"username_card": username_has, 'username': username}
        #     return HttpResponse(json.dumps(data))
        # -------上面是详细版------
        if hashers.check_password(post_data['password'], password_hash):
            # 生产加密盐用户
            # username_has = hashers.make_password(username)
            # # 加工为对象传给前端
            # data['username_card'] = username_has
            # data['username'] = username
            # 生成session 保存用户
            request.session['username'] = username
            request.session['user_id'] = User.objects.filter(username=username)[0].id
        else:
            data['code'] = 400
        return HttpResponse(json.dumps(data))


# 注册页面数据接收与注册帐号

def reg(request):
    # 返回token值给前端
    if request.method == 'GET':
        # 获取csrf_token的值
        csrf_token = get_token(request)
        # password_hash = hashers.make_password("123123")
        # print(hashers.check_password('123123', password_hash))
        # print(len(password_hash))

        return HttpResponse(csrf_token)
    if request.method == 'POST':

        # 得到json字符串 通过json.loads转换为字典，然后去其中的数据
        data = json.loads(request.body)['data']
        # 接收收到的请求
        username = data['username']
        password = data['password']
        phone = data['phone']
        # 生产加密盐密码
        pwd_has = hashers.make_password(password)
        # 判断下当前帐号是否存在，存在不让注册
        if User.objects.filter(username=username) or User.objects.filter(phone=phone):
            return HttpResponse('用户存在')
        User.objects.create(username=username, password=pwd_has, phone=phone)
        return HttpResponse('创建成功')


# 检查帐号，手机号等是否存在
def inspect(request):
    if request.method == 'GET':
        # 判断下当前请求的数据是帐号的还是手机号的，分别处理
        # 获取两个数据
        getUserName = request.GET.get('username', '')
        getPhone = request.GET.get('phone', '')
        # 如果为空不处理
        if not getUserName and not getPhone:
            return HttpResponse('用户名或手机号可以使用')
        # 如果发来的是帐号，核实是否存在
        if getUserName:
            userQuery = User.objects.filter(username=getUserName)
            if len(userQuery) > 0:
                data = json.dumps({"userBool": 1})
                return HttpResponse(data)
        # 如果发来的是手机号，核实是否存在
        if getPhone:
            PhoneQuery = User.objects.filter(phone=getPhone)
            if len(PhoneQuery) > 0:
                data = json.dumps({"phoneBool": 1})
                return HttpResponse(data)

    return HttpResponse('可以使用')


# 验证用户的session，获取用户数据
def session_ver(request):
    if request.method == 'GET':
        # 返回的数据
        data = {'code': 200}
        if 'pattern' in request.GET and request.GET.get('pattern') == 'delete':
            # 获取当前用户提交的注销名
            username = request.GET.get('username')
            del request.session['username']
            del request.session['user_id']
        # 验证当前登录用户是否有session
        if 'username' not in request.session or 'user_id' not in request.session:
            data['code'] = 400
            return HttpResponse(json.dumps(data))
        username = request.session.get('username', '没有username')
        user_id = request.session.get('user_id', '没有id')
        # 获取当前用户数据
        user_data = User.objects.filter(id=user_id, username=username)
        # 判断下当前用户是否存在
        if user_data:
            # 存在就获取他的信息，当然现在只有用户名有用，先获取它
            data['username'] = user_data[0].username
            data['user_id'] = user_data[0].id
            user = User.objects.filter(username=username)[0]
            # 获取用户的详细信息
            if not User_info.objects.filter(user=user):
                # 所有数据返回空
                data['nick_name'] = ''
                data['age'] = ''
                data['sex'] = ''
                data['id_card'] = ''
                return HttpResponse(json.dumps(data))
            # 存在就返回数据
            info = User_info.objects.filter(user=user)[0]
            data['nick_name'] = info.nick_name
            data['age'] = info.age
            data['sex'] = info.sex
            data['id_card'] = info.id_card
            data['bar_coin'] = info.bar_coin
            data['exp'] = info.exp
            data['portrait'] = str(info.portrait)
            print(str(info.portrait))
        return HttpResponse(json.dumps(data))
    if request.method == 'POST':
        return HttpResponse('提交成功')


#    获取用户详细信息
def info(request):
    if request.method == 'GET':
        # 创建返回的信息
        data = {'code': 200}
        # 验证当前用户是否存在
        if not request.session['username']:
            data['message'] = '用户不存在'
            data['code'] = 400
            return HttpResponse('data')
        # 获取当前用户表格
        user = User.objects.filter(username=request.session['username'])[0]
        # 获取当前提交的信息
        nick_name = request.GET['nick_name']
        age = request.GET['age']
        sex = request.GET['sex']
        id_card = request.GET['id_card']

        # 如果当前用户的资料不存在,直接保存
        if not User_info.objects.filter(user=user):
            # 判断当前提交的资料nick_name 是否唯一
            if User_info.objects.filter(nick_name=nick_name):
                data['message'] = '昵称已存在'
                data['code'] = 400
                return HttpResponse(json.dumps(data))
            # 当用户不存在时要验证身份证号码
            if User_info.objects.filter(id_card=id_card):
                data['message'] = '该身份证已经被注册'
                data['code'] = 400
                return HttpResponse(json.dumps(data))
            User_info.objects.create(user=user, nick_name=nick_name, age=age, sex=sex, id_card=id_card)
            data['message'] = '修改成功'
        if User_info.objects.filter(user=user):
            # 判断当前提交的资料nick_name 是否唯一
            if User_info.objects.filter(nick_name=nick_name) and User_info.objects.filter(user=user)[
                0].nick_name != nick_name:
                data['message'] = '昵称已存在'
                data['code'] = 400
                return HttpResponse(json.dumps(data))
            # 如果用户提交的身份证号码和自己的不一样就需要重新验证身份证
            if id_card and User_info.objects.filter(user=user)[0].id_card != id_card and User_info.objects.filter(
                    id_card=id_card):
                data['message'] = '该身份证已经被注册'
                data['code'] = 400
                return HttpResponse(json.dumps(data))
            user_info = User_info.objects.filter(user=user)[0]
            user_info.nick_name = nick_name
            user_info.age = age
            user_info.sex = sex
            user_info.id_card = id_card
            user_info.save()
            data['message'] = '修改成功'
        return HttpResponse(json.dumps(data))
    if request.method == 'POST':
        return HttpResponse('提交成功')


# 上传头像
def post_por(request):
    if request.method == 'GET':
        # 获取csrf_token的值
        csrf_token = get_token(request)
        return HttpResponse(csrf_token)
        # return render(request, 'test.html')
    if request.method == 'POST':
        # 放回的数据
        data = {'code': 200}
        file = request.FILES['file']
        file_name = file.name
        file_path = os.path.join(settings.MEDIA_ROOT, time.strftime("%Y-%m-%d", time.localtime()) + '-' + file_name)
        print(file_path)
        # 获取用户信息
        user = User.objects.filter(username=request.session.get('username'))[0]
        # 判断下用户是否填写过详细资料
        if not User_info.objects.filter(user=user):
            data['code'] = 400
            data['message'] = '上传失败：请填写详细资料后，再上传头像'
            return HttpResponse(json.dumps(data))
        with open(file_path, 'wb')as f:
            data_file = file.file.read()
            f.write(data_file)
        # 图片路径写入表格
        u_info = User_info.objects.filter(user=user)[0]
        u_info.portrait = file
        u_info.save()
        print(file)
        # 保存成功返回信息
        data['message'] = '头像保存成功'
        return HttpResponse(json.dumps(data))


# 获取用户的所有信息
def getUserData(request):
    if request.method == 'GET':
        # 返回的数据
        data = {'code': 200}
        user = User.objects.filter(username=request.session.get('username'), is_active=True)[0]
        # 判断当前用户是否填写了详细的资料
        if not User_info.objects.filter(user=user):
            print('我为空')
            data['message'] = '请填写详细资料再来创建主题'
            data['code'] = 400
            return HttpResponse(json.dumps(data))
        userInfo = User_info.objects.filter(user=user)[0]
        data['username'] = user.username
        data['user_id'] = user.id
        data['phone'] = user.phone
        data['id_card'] = userInfo.id_card
        data['portrait'] = str(userInfo.portrait)
        data['nick_name'] = userInfo.nick_name
        data['age'] = userInfo.age
        data['sex'] = userInfo.sex
        data['exp'] = userInfo.exp
        data['bar_coin'] = userInfo.bar_coin
        data['created_time'] = str(userInfo.created_time)[0:19]
        data['message'] = '获取个人资料成功'
        return HttpResponse(json.dumps(data))
