from django.urls import path
from .ueditor_view import get_ueditor_controller
from article import views

urlpatterns = [
    path('controller', get_ueditor_controller),
    # 提交文章内容创建新的主题
    path('p_art', views.writeArticle),
    # 获取用户的文章内容
    path('getArt', views.getArt),
    # 获取单个文章内容
    path('getOneArticle', views.getOneArticle),
    # 创建主题
    path('createBar', views.createBar),
    # 搜索主题
    path('search_bar', views.search_bar),
    # 获取bar的文章
    path('getBarArt', views.getBarArt),
    # 提交回帖内容创建新的回帖
    path('writeReply', views.writeReply),
    # 获取回帖成功
    path('getReply', views.getReply),
    # 获取主题
    path('getBarData', views.getBarData),
    # 设置主题
    path('setBar', views.setBar),
    # 上传头像
    path('postBarPortrait', views.postBarPortrait)
]
