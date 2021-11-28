<template>
    <div class="Theme InfoSet">
        <img class="mxd_icon" :src="'/django/media/'+barData.portrait" width="150" height="150">
        <span class="bar_data">
            <p class="bar_title">{{barData.bar_name}}</p>
            <p class="bar_text">{{barData.int}}</p>
            <button class="follow_but">点击关注</button>
            <button v-show="barUser()" class="follow_but" @click="toBarSet">设置主题介绍</button>
        </span>
        <ul class="title">
            <li class="host_li opint">今日热帖</li>
            <li class="opint" @click="getBarArticle">
                最新
            </li>
            <li class="opint">精品</li>
            <li class="opint">收藏</li>
            <router-link :to="{
                name:'write',
                query:{
                    bar_id:bar_id
                }
            }">
                <li>发布</li>
            </router-link>
        </ul>
        <el-input size="mini" class="search_bar" placeholder="主题内搜索" v-model="search_bar_data" clearable>
        </el-input>
        <img @click="Bar_search()" class="big_icon" src="../static/放大镜.png" width="20px" height="20px">
        <ul class="text">
            <li class="text_li" v-for="text in artData" :key="text.id">
                <router-link :to="{
                    name:'article',
                    query:{
                        bar_id:bar_id,
                        article_id :text.id
                    }
                }"><p class="mini_title">{{text.title}}<span class="active">140</span></p>
                </router-link>
                <p class="mini_text" v-html="hidden_img(text.content)"></p>
                <p class="time">{{text.updated_time.slice(0,19)}}</p>
                <hr class="split">
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
        name: "Theme",
        data() {
            return {
                search_bar_data: '',
                barData: '',
                artData: '',
                page: 0,
                number: 10,
                new_number: 10,
                loaded: false,
            }
        },
        computed: {
            bar_id() {
                return this.$route.query.bar_id
            }
        },
        methods: {
            // 主题内搜索
            Bar_search() {
                if (!this.search_bar_data) {
                    alert('搜索框不能为空')
                    return
                }
                axios.get('/django/article/search_bar', {
                    params: {
                        search_type: 'bar',
                        seachData: this.search_bar_data,
                        bar_id: this.bar_id
                    }
                }).then(res => {
                    this.artData = res.data['art_data']
                    console.log(res.data['art_data'])
                }, err => {
                    console.log(err.message)
                })
            },
            // 主题主权限：显示主题设置内容
            barUser() {
                if (!this.$store.state.username === this.barData.barUserName) {
                    return false;
                }
                if (this.$store.state.username === this.barData.barUserName) {
                    return true;
                }
            },
            // 去设置主题详情
            toBarSet() {
                this.$router.push({
                    name: 'barset',
                    query: {
                        bar_id: this.bar_id
                    }
                })
            },
            // 获取主题列表参数
            getBarArticle() {
                axios.get('/django/article/getBarArt', {
                    params: {
                        bar_id: this.bar_id,
                    }
                }).then(res => {
                    this.barData = res.data['bar_data']
                    // 获取前10个文章
                    this.artData = res.data['art_data'].slice(this.page, this.number)
                }, err => {
                    console.log(err.message)
                })
            },
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
                return this.getData(text)
            },
            // 检查内容为空，返回无
            getData(data) {
                if (data.length === 0) {
                    return '无'
                } else if (data) {
                    return data
                }
            },
            // 加载更多的内容
            onLoad() {
                this.page = this.page + 10
                this.new_number = this.new_number + 10
                axios.get('/django/article/getBarArt', {
                    params: {
                        bar_id: this.bar_id
                    }
                }).then(res => {
                    let new_art = res.data["art_data"].slice(this.page, this.new_number)
                    if (new_art.length === 0) {
                        this.loaded = true
                    }
                    new_art.forEach(text => {
                        this.artData.push(text)
                    })
                }, err => {
                    console.log(err.message)
                })
            },
        },
        created() {
            this.getBarArticle()
        }
    }
</script>

<style scoped>
    * {
        font-family: 思源黑体R;
        color: #414157;
    }

    a {
        text-decoration: none;
    }

    .Theme {
        width: 1160px;
        height: 850px;
        background-color: white;
        border-radius: 5px;
    }

    .mxd_icon {
        border-radius: 5px;
        border: solid 3px white;
        position: absolute;
        top: -40px;
        left: 30px;
        box-shadow: 0px 4px 3px rgba(0, 0, 0, 0.3);
    }

    .bar_data {
        position: absolute;
        left: 200px;
    }

    .follow_but {
        position: relative;
        top: -105px;
        left: 100px;
        background-color: #414157;
        color: #fdde5e;
        border-radius: 5px;
        padding: 0px 20px;
        font-size: 16px;
        border: solid 1px #414157;
        font-family: 思源黑体L;
    }

    .bar_title {
        color: #262c3e;
        font-size: 30px;
        font-family: 思源黑体R;
        position: relative;
        top: 10px
    }

    .bar_text {
        color: #262c3e;
        font-size: 20px;
        font-family: 思源黑体L;
        position: relative;
        top: -20px;

    }

    .title {
        position: relative;
        top: 130px;
        left: 0;
        background-color: #414157;
        height: 64px;
    }

    .title li {
        display: inline;
        padding: 21px 50px;
        font-size: 24px;
        position: relative;
        /*background-color: #414157;*/
        /*position: absolute;*/
        color: white;
        font-family: 思源黑体L;
        top: 14px;
        left: -40px;
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

    .title li:hover {
        background-color: #fdde5e;
        color: #262c3e;
    }

    .search_bar {
        width: 170px;
        position: absolute;
        top: 165px;
        left: 840px;
    }

    .big_icon {
        position: absolute;
        top: 168px;
        left: 1015px;
    }

    .text {
        position: relative;
        top: 150px;
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
        font-size: 20px;
        color: #626264;
        padding: 0;
        margin: -15px 0;
    }

    .split {
        padding: 0;
        margin: 0;
        height: 1px;
        border: none;
        border-top: 1px solid #e5e5e5;
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

    .text {
        height: 630px;
        overflow: auto;
        overflow-x: hidden;
        position: relative;
        top: 120px;
    }

    .time {
        position: relative;
        left: 945px;
        top: -20px;
        padding: 0;
        margin: 0;
        font-family: 思源黑体L;
        font-size: 14px;
    }

    .center {
        text-align: center;
    }

    .opint {
        cursor: pointer;
    }
</style>