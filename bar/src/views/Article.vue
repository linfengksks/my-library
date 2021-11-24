<template>
    <div class="Theme">
        <!--头部导航栏-->
        <div>
            <ul class="title">
                <li class="opint">最新<span class="split"></span></li>
                <li class="opint">精品<span class="split"></span></li>
                <li class="opint">收藏</li>
            </ul>
            <el-input size="mini" class="search_bar" placeholder="主题内搜索" v-model="search_bar_data" clearable>
            </el-input>
            <img class="big_icon" src="../static/放大镜.png" width="20px" height="20px">
            <img class="mxd_icon" src="../static/冒险岛头像.png" width="100" height="100">
            <span class="bar_data">
                <p class="y_back"></p>
                <span class="mxd_name">
                   <router-link :to="{
                       name:'theme',
                       query:{
                           bar_id:this.$route.query.bar_id
                        }
                   }"> <p class="bar_title">冒险岛</p></router-link>
            <p class="bar_text">爱我就来冒险岛!</p>
            <button class="follow_but">点击关注</button>
                </span>

        </span>

        </div>
        <!--主体内容-->
        <div class="article_content">
            <!--文章内容-->
            <div class="article_com">
                <p class="aut_title">{{author_data.title}}</p>
                <hr class="opacity_30">
                <div class="art_box">
                    <!--用户的信息栏-->
                    <div class="user_box">
                        <p class="Land1">楼主</p>
                        <span class="aut_info">
                    <img class="aut_por" :src="getPortrait(author_data.portrait)" alt="作者头像" width="100"
                         height="100">
                    <p class="nickName">{{author_data.nick_name}}</p>
                    <p class="Grade_name">菜鸡出道<span class="Grade2">0</span></p>
                    </span>

                    </div>
                    <!--用户文章内容-->
                    <div class="content_box">
                        <p class="art_con" v-html="author_data.content"></p>
                        <p class="art_time">{{author_data.up_time}}-发帖</p>
                    </div>

                </div>
                <hr class="opacity_30 hr_position">
            </div>
            <!--回帖内容-->
            <div class="reply_com">
                <ul class="reply_ul">
                    <li v-for="(r,index) in replyData" :key="r.id">
                        <div class="art_box">
                            <!--用户的信息栏-->
                            <div class="user_box user_box2 ">
                                <p class="Land2">{{index+1}}楼</p>
                                <span class="aut_info">

                    <img class="aut_por" :src="getPortrait(r.portrait)" alt="用户头像" width="100"
                         height="100">
                    <p class="nickName">{{r.nick_name}}</p>
                    <p class="Grade_name">菜鸡出道<span class="Grade2">0</span></p>
                    </span>
                            </div>
                            <!--用户文章内容-->
                            <div class="content_box">
                                <p class="art_con" v-html="r.reply_text"></p>
                                <p class="art_time">{{author_data.up_time}}-回帖</p>
                            </div>
                        </div>
                        <hr class="reply_hr"/>
                    </li>
                </ul>

                <div class="reply_ue">
                    <h3 class="reply_h3"><i class="el-icon-edit-outline"></i><span>发表回帖</span></h3>
                    <vue-ueditor-wrap class="ueditor" v-model='replyText' :config="ueConfig"></vue-ueditor-wrap>
                    <el-button @click="postReply" class="but1" type="primary" round>发表</el-button>
                </div>

            </div>
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    import VueUeditorWrap from 'vue-ueditor-wrap'

    export default {
        name: "Article",
        components: {
            VueUeditorWrap
        },
        data() {
            return {
                search_bar_data: '',
                // 作者的资料
                author_data: '',
                // 第一次获取资料
                firstExe: true,
                // 第一次进入刷新
                oneRefresh: true,
                replyText: '',
                // ueditor 设置信息
                ueConfig: {
                    // 初始容器高度
                    initialFrameHeight: 300,
                    // 初始容器宽度
                    initialFrameWidth: '800',
                    // 上传文件接口
                    enableAutoSave: false,
                    elementPathEnable: false,
                    wordCount: false,
                    UEDITOR_HOME_URL: '/UEditor/',
                    serverUrl: 'http://localhost:8080/django/article/controller',// 上传文件接口
                    toolbars: [
                        [
                            'undo', //撤销
                            'bold', //加粗
                            'indent', //首行缩进
                            'italic', //斜体
                            'underline', //下划线
                            'strikethrough', //删除线
                            'subscript', //下标
                            'fontborder', //字符边框
                            'superscript', //上标
                            'formatmatch', //格式刷
                            'fontfamily', //字体
                            'fontsize', //字号
                            'justifyleft', //居左对齐
                            'justifycenter', //居中对齐
                            'justifyright', //居右对齐
                            'justifyjustify', //两端对齐
                            'insertorderedlist', //有序列表
                            'insertunorderedlist', //无序列表
                            'lineheight',//行间距
                            'simpleupload', //单图上传
                            'insertimage', //多图上传
                            'link', //超链接
                            'insertvideo', //视频
                        ]
                    ],
                },
                replyData: '',
            }
        },
        watch: {
            // 当文章id发生改变时调用getArtcle获取新内容
            article_id() {
                if (this.article_id) {
                    this.getArtcle()
                }
            }
        },
        computed: {
            article_id() {
                return this.$route.query.article_id
            }
        },
        created() {
            this.oneGetArtcle()
            this.getReply()
        },
        methods: {
            // 获取回帖
            getReply() {
                // 请求服务器返回数据
                axios.get('/django/article/getReply', {
                    params: {
                        art_id: this.article_id
                    }
                }).then(res => {
                    if (res.data['code'] === 200) {
                        console.log(res.data)
                        this.replyData = res.data['replyData']
                    } else if (res.data['code'] === 400) {
                        console.log(res.data['message'])
                    }
                }, err => {
                    console.log(err.message)
                })
            },
            // 发布回帖
            postReply() {
                // if (!sessionStorage.getItem('user_id')) {
                //     console.log(sessionStorage.getItem('user_id'))
                //     alert('未登录无法回帖')
                //     return
                // }
                // 设置csrf_token
                axios.get('http://localhost:8080/django/user/session').then(res => {
                    const csrf_token = res.data
                    window.sessionStorage.setItem('csrf_token', csrf_token)
                })
                //处理提交的数据
                let data = {
                    art_id: this.article_id,
                    replyText: this.replyText,
                }
                //上传回帖内容到服务器
                axios({
                    method: 'post',
                    url: 'http://localhost:8080/django/article/writeReply',
                    data: data,
                    headers: {
                        //将csrf_token放在请求头中
                        'X-CSRFToken': window.sessionStorage.getItem("csrf_token")
                    }
                }).then(
                    res => {
                        if (res.data['code'] === 400) {
                            alert(res.data['message'])
                        } else if (res.data['code'] === 200) {
                            alert(res.data['message'])
                            // this.$router.push({
                            //     name: 'theme',
                            //     query: {
                            //         bar_id: this.$route.query.bar_id
                            //     }
                            // })
                            // location.reload()
                        }
                    }, err => {
                        console.log(err.message)
                    })
            },
            // 如果头像图片没有信息就不返回图片地址
            getPortrait(url) {
                if (!url) {
                    return url
                } else if (url) {
                    url = '/django/media/' + url
                    return url
                }
            },
            // 获取文章内容
            getArtcle() {
                // console.log(this.article_id)
                axios.get('http://localhost:8080/django/article/getOneArticle', {
                    params: {
                        article_id: this.article_id
                    }
                }).then(res => {
                    if (res.data['code'] === 200) {
                        this.author_data = res.data
                        console.log(res.data)
                    }
                }, err => {
                    console.log(err.message)
                })
                this.firstExe = false

            },
            // 创建页面时获取一次文章内容内容
            oneGetArtcle() {
                if (this.firstExe) {
                    this.getArtcle()
                }
            }
        },
    }
</script>

<style scoped>
    * {
        font-family: 思源黑体R;
        color: #414157;
    }

    .Theme {
        width: 1160px;
        height: 850px;
        background-color: white;
        border-radius: 5px;
    }

    a {
        text-decoration: none;
    }

    .reply_com li {
        list-style: none;
    }

    .mxd_icon {
        position: relative;
        top: -130px;
        left: 10px;
        border-radius: 5px;
        border: solid 3px white;
        box-shadow: 0px 4px 3px rgba(0, 0, 0, 0.3);
    }

    .hr_position {
        position: relative;
        top: -18px
    }

    .y_back {
        position: absolute;
        top: -112px;
        left: -84px;
        background-color: #fdde5e;
        padding: 32px 102px;
    }

    .bar_data {
        position: absolute;
        left: 200px;
    }

    .follow_but {
        position: relative;
        top: -90px;
        left: 80px;
        background-color: #414157;
        color: #fdde5e;
        border-radius: 5px;
        padding: 0px 20px;
        font-size: 12px;
        border: solid 1px #414157;
        font-family: 思源黑体L;
    }

    .follow_but:hover {
        background-color: #e92a5b;
        color: white;
        border-color: #ea1048;
    }

    .bar_title {
        color: #262c3e;
        font-size: 24px;
        font-family: 思源黑体R;
        position: relative;
        top: 10px
    }

    .bar_text {
        color: #262c3e;
        font-size: 16px;
        font-family: 思源黑体L;
        position: relative;
        top: -20px;

    }

    .title {
        position: relative;
        top: -16px;
        background-color: #414157;
        border-radius: 5px 5px 0 0;
        height: 64px;
    }

    .title li {
        display: inline;
        padding: 20px 50px;
        font-size: 24px;
        position: relative;
        /*background-color: #414157;*/
        color: white;
        font-family: 思源黑体L;
        top: 14px;
        left: 280px;
    }

    .split {
        position: relative;
        left: 50px;
        border-color: white;
        border-style: solid;
        border-width: 0 0 0 1px;
        opacity: 0.3;
    }

    .split:hover {
        opacity: 0;
    }

    .opacity_30 {
        opacity: 0.3;
    }

    .title li:hover {
        background-color: #fdde5e;
        color: #414157;
    }

    .mxd_name {
        position: relative;
        top: -125px;
        left: -70px

    }

    .title .split {
        color: white;
        width: 1px;
        height: 10px;
    }

    .title .host_li {
        background-color: #fdde5e;
        color: #414157;
    }

    .search_bar {
        width: 170px;
        position: absolute;
        left: 900px;
        top: 20px;
    }

    .big_icon {
        position: absolute;
        top: 23px;
        left: 1080px;
    }

    .article_com {
        position: relative;
        top: 0px;
    }

    .art_box {
        position: relative;
        top: -9px;
        display: -webkit-box;
    }

    .user_box {
        padding: 0;
        margin: 0;
        width: 200px;
        background-color: #cecedd;
    }

    .content_box {
        padding: 0;
        margin: 0;
        width: 960px;
        background-color: white;
    }

    .Land1 {
        background-color: #414157;
        color: #fdde5e;
        border-radius: 0 0 0 5px;
        width: 40px;
        text-align: center;
        font-size: 14px;
        position: absolute;
        left: 160px;
        top: -15px;
    }

    .Land2 {
        background-color: #414157;
        color: white;
        border-radius: 0 0 0 5px;
        width: 40px;
        text-align: center;
        font-size: 14px;
        position: absolute;
        left: 160px;
        top: -15px;
    }

    .Grade2 {
        font-size: 16px;
        position: relative;
        left: 60px;
        top: -25px;
        background-image: url("../static/等级图标.png");
        background-position: 3px 3px;
        background-size: 20px;
        background-repeat: no-repeat;
        padding: 4px 10px 5px 8px;
        color: #bb8738;
        text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.3);

    }

    .Grade_name {
        font-size: 14px;
        width: 60px;
        height: 16px;
        background-color: #414157;
        padding: 5px 30px 7px 10px;
        color: white;
        border-radius: 3px;
        background-image: linear-gradient(#7a7a8e, #414157);
        position: relative;
        left: 50%;
        margin-left: -50px;
        margin-top: 5px;
        /*margin-bottom: 100px;*/
    }

    .aut_por {
        border: solid 1px #87879a;
        padding: 3px;
        background-color: white;
        border-radius: 3px;
        position: relative;
        left: 50%;
        margin-left: -55px;
    }

    .nickName {
        text-align: center;
        padding: 0;
        margin: 0;
    }

    .aut_info {
        position: relative;
        top: 50px;
    }

    .aut_title {
        font-size: 26px;
        margin: 0;
        padding: 0 0 0 10px;
    }

    .art_con {
        font-size: 20px;
        padding: 0 30px;
        text-indent: 20px;
        letter-spacing: 1px;
        position: relative;
        left: -10px;
    }

    .art_time {
        position: relative;
        bottom: 0px;
        float: right;
        padding: 0 30px;
        color: #7e7e9c;
        font-family: 思源黑体L;
        letter-spacing: 0.7px;
        margin-top: 130px;
    }

    .article_content {
        height: 760px;
        overflow: auto;
        overflow-x: hidden;
        position: relative;
        top: -120px;
    }

    .reply_com {
        padding: 0;
        margin: -18px 0;
    }

    .ueditor {
        position: relative;
        left: 50%;
        margin-left: -400px;
    }

    .reply_ue {
        background-color: #f7f8fa;
        width: 1160px;
        height: 500px;
        position: relative;
        top: -36px;
    }

    .but1 {
        color: white;
        background-color: #414157;
        border-color: #414157;
        position: relative;
        left: 900px;
        top: 10px;
    }

    .but1:hover {
        background-color: #262c3e;
        border-color: #262c3e;
    }

    .reply_h3 {
        position: relative;
        left: 180px;
        padding: 20px 0 0 0;
    }

    .reply_ul {
        position: relative;
        top: -8px;
        left: -40px;
    }

    .reply_hr {
        position: relative;
        padding: 0px;
        margin: -1px;
        top: -9px;
        opacity: 0.3;
    }

    .opint {
        cursor: pointer;
    }

    /*针对IE的设置*/

    @media screen and (-ms-high-contrast: active), (-ms-high-contrast: none) {
        /* IE10-specific styles go here */
        .art_con {
            position: relative;
            left: 0px;
            top: 0px;
            margin: 0 0 -120px 0;
        }

        .art_time {
            position: relative;
            bottom: 0px;
            float: none;
            left: 890px;
            padding: 0 30px;
            color: #7e7e9c;
            font-family: 思源黑体L;
            letter-spacing: 0.7px;
            margin-top: 130px;
        }

        .user_box {
            padding: 0;
            margin: 0;
            width: 200px;
            background-color: #cecedd;
        }

        .user_box2 {
            padding: 0;
            margin: 0;
            width: 208.8px;
            background-color: #cecedd;
        }

        .hr_position {
            position: relative;
            top: -18px;
        }

        .Grade2 {
            font-size: 16px;
            position: relative;
            left: 60px;
            top: -18px;
            background-image: url("../static/等级图标.png");
            background-position: 2px 3px;
            background-size: 20px;
            background-repeat: no-repeat;
            padding: 4px 10px 5px 8px;
            color: #bb8738;
            text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.3);

        }

        .bar_text {
            color: #262c3e;
            font-size: 16px;
            font-family: 思源黑体L;
            position: relative;
            top: -10px;
            left: 3px;
        }

        .follow_but {
            position: relative;
            top: -75px;
            left: 80px;
            background-color: #414157;
            color: #fdde5e;
            border-radius: 5px;
            padding: 3px 20px;
            font-size: 12px;
            border: solid 1px #414157;
            font-family: 思源黑体L;
        }

        .reply_hr {
            position: relative;
            padding: 0px;
            margin: -1px;
            top: -9px;
            opacity: 0.3;
            width: 1160px;
        }

        .aut_info {
            position: relative;
            top: 0px;
        }

        .art_box {
            position: relative;
            top: -9px;
            display: -webkit-box;
            display: -ms-flexbox;
        }

        .Land1 {
            background-color: #414157;
            color: #fdde5e;
            border-radius: 0 0 0 5px;
            width: 40px;
            text-align: center;
            font-size: 14px;
            position: absolute;
            left: 157px;
            top: -15px;
        }

        .Land2 {
            border-radius: 0 0 0 5px;
            width: 40px;
            left: 157px;
            top: -15px;
        }

        .title li {
            display: inline;
            padding: 19px 50px 18px 50px;
            font-size: 24px;
            position: relative;
            /*background-color: #414157;*/
            color: white;
            font-family: 思源黑体L;
            top: 19px;
            left: 280px;
        }
    }

</style>