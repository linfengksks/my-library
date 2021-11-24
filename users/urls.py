from django.urls import path

from users import views

urlpatterns = [
    # 配置注册视图函数http://127.0.0.1:8000/user/reg
    path('reg', views.reg),
    # 配置登录视图函数http://127.0.0.1:8000/user/login
    path('login', views.login),
    # 配置检查帐号手机号是否存在的api
    path('inspect', views.inspect),
    # 验证session，获取用户信息 http://127.0.0.1:8000/user/session
    path('session', views.session_ver),
    # 获取用户信息
    path('info', views.info),
    # 上传头像
    path('post_por', views.post_por),
    # 获取用户的所有信息
    path('getUserData', views.getUserData),
]
