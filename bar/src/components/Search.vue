<template>
    <div class="ThemeInit Theme">
        <ul class="title">
            <li class="host_li">今日热帖</li>
            <li>最新</li>
            <li>收藏</li>
            <li>
                <router-link to="createBar">创建主题</router-link>
            </li>

        </ul>
        <p style="padding: 0 20px">搜索结果 :</p>
        <ul class="text">
            <li class="text_li" v-for="text in resultData['art_data']" :key="text.id">
                <router-link :to="{
                    name:'article',
                    query:{
                        article_id :text.id
                    }
                }"><p class="mini_title">{{text.title}}<span class="active">140</span></p>
                </router-link>
                <p class="mini_text" v-html="hidden_img(text.content)"></p>
                <p class="time">{{text.updated_time.slice(0,19)}}</p>
                <hr class="split">
            </li>
            <li class="text_li" v-for="text in resultData['bar_data']" :key="text.id">
                <router-link :to="{
                    name:'theme',
                    query: {
                        bar_id:text.id
                    }
                }"><p class="mini_title">{{text.bar_name}}<span class="active">主题</span></p></router-link>
                <p class="mini_int">简介：{{text.int}}</p>
                <p class="time2">{{text.created_time.slice(0,19)}}</p>
                <hr class="split"/>
            </li>
            <div class="center loaded" @scroll="scrollEvent()">
                <el-button v-show="!loaded" @click="onLoad" ref="loading">加载更多</el-button>
                <p v-show="loaded">加载完毕，没有更新的内容了</p></div>
        </ul>

    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "Search",
        data() {
            return {
                page: 0,
                numbar: 5,
                texts: '',
                loaded: false,
            }
        },
        computed: {
            resultData() {
                console.log(this.$store.state.resultData['art_data'])
                return this.$store.state.resultData
            }
        },
        methods: {
            // 屏蔽图片标签
            hidden_img(text) {
                // let text = '<p>大萨<img src="/django/media/冒险岛头像_20211102131046_647.png" title="" alt="冒险岛头像.png"/>德啊大萨达按时大多数<img src="/django/media/广告1_20211102131057_958.png" title="" alt="广告1.png"/>十大的撒大萨达大萨达</p>'
                // console.log(text.indexOf('<img'))
                // 如果文本内容没有<img标签，就直接返回原始内容
                if (text.search('<img') === -1) {
                    return text
                }
                // 有img，就执行下面循环去除img标签的代码
                for (let i = 0; text.search('<img') != -1; i++) {
                    let index1 = text.indexOf('<img')
                    let index9 = text.indexOf('/>')
                    text = text.slice(0, index1) + text.slice(index9 + 2)
                }
                // 注意是最后返回文本，不要在循环内返回，不然第一次就会被取消掉
                return text
            },
            //  滚动条到元素后触发函数加载
            scrollEvent() {
                console.log('滚动被触发')
                // let e = this.$refs.loading
                // // if (scrollDiv.scrollTop + scrollDiv.offsetHeight >= scrollDiv.scrollHeight) {
                // if (e.scrollTop + e.offsetHeight > e.scrollHeight - 100) {
                //     console.log('滚动被触发')
                //     this.onLoad()
                // }
            },
            // 加载更多的内容
            onLoad() {
                this.page = this.page + 5
                this.numbar = this.numbar + 5
                axios.get('http://localhost:8080/django/article/getArt').then(res => {
                    let new_texts = res.data["article_list"].slice(this.page, this.numbar)
                    if (new_texts.length === 0) {
                        this.loaded = true
                    }
                    new_texts.forEach(text => {
                        this.texts.push(text)
                    })
                }, err => {
                    console.log(err.message)
                })
            },
            // 加载前五条信息
            getArt() {
                //    发送axios请求获取当前用户的文章
                axios.get('http://localhost:8080/django/article/getArt').then(res => {
                    this.texts = res.data["article_list"].slice(this.page, this.numbar)
                    // console.log(res.data['message'])
                }, err => {
                    console.log(err.message)
                })
            }
        },
        created() {
            // this.getArt()
        }
    }
</script>

<style scoped>
    * {
        font-family: 思源黑体R;
        color: #414157;
    }

    .ThemeInit {
        width: 1160px;
        height: 850px;
        background-color: white;
        border-radius: 5px;
    }

    .title {
        position: relative;
        top: -16px;
        background-color: #414157;
        border-radius: 5px 5px 0 0;
        height: 64px;
    }

    .center {
        text-align: center;
    }

    .title li {
        display: inline;
        padding: 20px 50px;
        font-size: 24px;
        position: relative;
        background-color: #414157;
        color: white;
        font-family: 思源黑体L;
        top: 14px;
        left: -40px;
        transition: background 0.2s, color 0.2s;
        -webkit-transition: background 0.2s, color 0.2s;
    }

    .title a {
        font-family: 思源黑体L;
        color: white;
    }

    .title a:hover {
        background-color: #fdde5e;
        color: #414157;

    }

    .title li:hover {
        background-color: #fdde5e;
        color: #414157;

    }

    .title .split {
        color: white;
        width: 1px;
        height: 10px;
    }

    .title .host_li {
        background-color: #fdde5e;
        color: #414157;
        border-radius: 5px 0 0 0;
    }

    .title .host_li2 {
        background-color: #fdde5e;
        color: #414157;
    }

    .text {
        position: relative;
        top: 0px;
        list-style: none;
        left: -20px;
    }

    .mini_title {
        font-size: 30px;
        padding: 0;
        margin: 0;
    }

    .mini_text {
        position: relative;
        font-family: 思源黑体L;
        font-size: 16px;
        color: #626264;
        padding: 0 10px;
        margin: -20px 0;
        top: 10px
    }

    .mini_int {
        position: relative;
        font-family: 思源黑体L;
        font-size: 16px;
        color: #626264;
        padding: 0 3px;
        margin: -20px 0;
        top: 20px
    }

    .split {
        padding: 0;
        width: 100%;
        margin: 0;
        border: none;
        border-top: 1px solid #e5e5e5;
        position: relative;
        top: -20px;
    }

    .text_li {
        padding: 10px 0;
    }

    .active {
        position: relative;
        top: -10px;
        left: 5px;
        color: #404040;
        font-size: 20px;
        padding: 18px 18px 18px 12px;
        background-image: url("../static/回帖数背景.png");
        background-size: 60px;
        background-repeat: no-repeat;
    }

    li a {
        text-decoration: none;
    }

    .text {
        height: 650px;
        line-height: 30px;
        overflow: auto;
        overflow-x: hidden;
    }

    .time {
        position: relative;
        left: 945px;
        top: -20px;
        font-family: 思源黑体L;
        font-size: 14px;
    }

    .time2 {
        position: relative;
        left: 945px;
        top: -5px;
        font-family: 思源黑体L;
        font-size: 14px;
    }
</style>