<template>
    <div class="Write Theme">
        <div class="write_pos">
            <h2 class="title">发布文章</h2>
            <p class="title_text">标题：
                <el-input class="title_input"
                          placeholder="请输入文章的标题(5~100字)"
                          v-model="title"
                          clearable>
                </el-input>
            </p>

            <vue-ueditor-wrap class="ueditor" v-model='text' :config="ueConfig"></vue-ueditor-wrap>
            <div class="but">
                <el-button @click="upArticle" class="but1" type="primary" round>提交</el-button>
                <el-button class="but1" type="primary" round>返回</el-button>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import VueUeditorWrap from 'vue-ueditor-wrap'
    // 写文章的组件
    export default {
        name: "Write",
        components: {
            VueUeditorWrap
        },
        data() {
            return {
                title: '',
                text: '',
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
                }
            }
        },
        methods: {
            upArticle() {
                // 设置csrf_token
                axios.get('http://localhost:8080/django/user/session').then(res => {
                    const csrf_token = res.data
                    window.sessionStorage.setItem('csrf_token', csrf_token)
                })
                //处理提交的数据
                let data = {
                    title: this.title,
                    text: this.text,
                    bar_id: this.$route.query.bar_id
                }
                axios({
                    method: 'post',
                    url: 'http://localhost:8080/django/article/p_art',
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
                            this.$router.push({
                                name: 'theme',
                                query: {
                                    bar_id: this.$route.query.bar_id
                                }
                            })
                            location.reload()
                        }
                    }, err => {
                        console.log(err.message)
                    })

            }
        }
    }
</script>

<style scoped>
    .Write {
        width: 1160px;
        height: 850px;
        background-color: white;
        border-radius: 5px;

    }

    .title_input {
        width: 748px;
    }

    .title {
        position: relative;
        left: 180px;
        padding: 0 0 30px 0;
    }

    .title_text {
        position: relative;
        left: 180px;
    }

    .ueditor {
        position: relative;
        left: 50%;
        margin-left: -400px;
    }

    .but {
        position: relative;
        left: 80%;
        margin-left: -120px;
        padding: 30px 0 0 0;
    }

    .but1 {
        background-color: #414157;
        border-color: #414157;
    }

    .but1:hover {
        background-color: #262c3e;
        border-color: #262c3e;
    }

    .write_pos {
        position: relative;
        top: 80px;
    }
</style>