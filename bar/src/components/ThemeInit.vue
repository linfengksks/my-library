<template>
  <div class="ThemeInit Theme">
    <ul class="title-nav">
      <li class="host_li"><a href="#">今日热帖</a></li>
      <li @click.prevent="sortData('newest')"><a href="#">最新</a></li>
      <li><a href="#">收藏</a></li>
      <li>
        <router-link class="createBar" to="createBar"> 创建主题 </router-link>
      </li>
    </ul>
    <!-- 文章内容 -->
    <ul class="text">
      <!-- 标题 -->
      <li class="text_li" v-for="text in texts" :key="text.id">
        <router-link
          :to="{
            name: 'article',
            query: {
              article_id: text.id,
              bar_id: text.bar_id,
            },
          }"
          ><div class="mini_title">
            {{ text.title }}
            <!-- 获取回帖数并显示当前回帖数 -->
            <div class="reply-img">
              20
              <!-- <img src="../static/回帖数背景.png" alt="回帖图标" /> -->
            </div>
          </div>
        </router-link>
        <!-- 文章内容 -->
        <div class="mini_text" v-html="hidden_img(text.content)"></div>
        <!-- 文章创建时间 -->
        <p class="Ctime">{{ text.created_time.slice(0, 19) }}</p>
      </li>
      <div class="center loaded" @scroll="scrollEvent()">
        <el-button v-show="!loaded" @click="onLoad" ref="loading"
          >加载更多</el-button
        >
        <p v-show="loaded">加载完毕，没有更新的内容了</p>
      </div>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
// 引入重置样式表
import "../static/css/reset.css";
// 组件样式
import "../static/css/components/ThemeInit.css";
export default {
  name: "ThemeInit",
  data() {
    return {
      page: 0,
      numbar: 5,
      texts: "",
      loaded: false,
    };
  },
  methods: {
    // 对数据排序
    sortData(sort) {
      if (sort === "newest") {
        axios
          .get("http://localhost:8080/django/article/getArt", {
            params: {
              sort: sort,
            },
          })
          .then(
            (res) => {
              this.texts = res.data["article_list"].slice(
                this.page,
                this.numbar
              );
            },
            (err) => {
              console.log(err.message);
            }
          );
      }
    },
    // 屏蔽图片标签
    hidden_img(text) {
      // let text = '<p>大萨<img src="/django/media/冒险岛头像_20211102131046_647.png" title="" alt="冒险岛头像.png"/>德啊大萨达按时大多数<img src="/django/media/广告1_20211102131057_958.png" title="" alt="广告1.png"/>十大的撒大萨达大萨达</p>'
      // console.log(text.indexOf('<img'))
      // 如果文本内容没有<img标签，就直接返回原始内容
      if (text.search("<img") === -1) {
        return text;
      }
      // 有img，就执行下面循环去除img标签的代码
      for (let i = 0; text.search("<img") != -1; i++) {
        let index1 = text.indexOf("<img");
        let index9 = text.indexOf("/>");
        text = text.slice(0, index1) + text.slice(index9 + 2);
      }
      // 注意是最后返回文本，不要在循环内返回，不然第一次就会被取消掉
      return text;
    },
    //  滚动条到元素后触发函数加载
    scrollEvent() {
      console.log("滚动被触发");
      // let e = this.$refs.loading
      // // if (scrollDiv.scrollTop + scrollDiv.offsetHeight >= scrollDiv.scrollHeight) {
      // if (e.scrollTop + e.offsetHeight > e.scrollHeight - 100) {
      //     console.log('滚动被触发')
      //     this.onLoad()
      // }
    },
    // 加载更多的内容
    onLoad() {
      this.page = this.page + 5;
      this.numbar = this.numbar + 5;
      axios.get("http://localhost:8080/django/article/getArt").then(
        (res) => {
          let new_texts = res.data["article_list"].slice(
            this.page,
            this.numbar
          );
          if (new_texts.length === 0) {
            this.loaded = true;
          }
          new_texts.forEach((text) => {
            this.texts.push(text);
          });
        },
        (err) => {
          console.log(err.message);
        }
      );
    },
    // 加载前五条信息
    getArt() {
      //    发送axios请求获取当前用户的文章
      axios.get("http://localhost:8080/django/article/getArt").then(
        (res) => {
          this.texts = res.data["article_list"].slice(this.page, this.numbar);
        },
        (err) => {
          console.log(err.message);
        }
      );
    },
  },
  created() {
    this.getArt();
  },
};
</script>

<style scoped>

</style>