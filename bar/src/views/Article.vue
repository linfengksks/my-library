<template>
  <div class="Article InfoSet">
    <!--头部导航栏-->
    <div class="bar-nav-wrapper">
      <!-- 主题信息 -->
      <div class="bar-info">
        <!-- 主题头像 -->
        <div class="bar-por">
          <img
            class="mxd_icon"
            src="../static/冒险岛头像.png"
            width="100px"
            height="100px"
          />
        </div>
        <div class="bar-title-wrapper">
          <!--主题名 -->
          <div class="bar-title">
            <router-link
              :to="{
                name: 'theme',
                query: {
                  bar_id: this.$route.query.bar_id,
                },
              }"
              ><span>冒险岛</span></router-link
            >

            <el-button type="primary" class="follow-but">点击关注</el-button>
          </div>
          <!-- 主题简介 -->
          <div class="bar-content">爱我就来冒险岛!</div>
          <!-- 点击按钮 -->
        </div>
      </div>
      <div>
        <!-- 导航条 -->
        <ul class="article-nav">
          <li class="opint"><a href="#">最新</a></li>
          <li class="opint"><a href="#">精品</a></li>
          <li class="opint"><a href="#">收藏</a></li>
        </ul>
      </div>
      <!-- 搜索框 -->
      <div class="search-bar">
        <el-input
          size="mini"
          class="search-input"
          placeholder="主题内搜索"
          v-model="search_bar_data"
          clearable
        >
        </el-input>
        <img
          class="big-icon"
          src="../static/放大镜.png"
          width="20px"
          height="20px"
        />
      </div>
    </div>
    <div class="body-wrapper">
      <!--主体内容-->
      <div class="body-con">
        <!-- 文章标题 -->
        <div class="art-title-wrapper">
          <!-- 标题 -->
          <div class="art-title">
            {{ author_data.title }}
          </div>
          <!-- 右侧功能 -->
          <div class="art-title-btn">
            <el-row>
              <el-button plain>只看楼主</el-button>
            </el-row>
            <el-row>
              <el-button plain>回复</el-button>
            </el-row>
          </div>
        </div>
        <!-- 下面用户信息和文章内容 -->
        <div class="atr-con-wrapper">
          <!-- 左侧用户信息 -->
          <div class="art-user">
            <!-- 楼层 -->
            <div class="Land1">楼主</div>
            <div class="user-por">
              <img
                class="aut_por"
                :src="getPortrait(author_data.portrait)"
                alt="作者头像"
                width="100"
                height="100"
              />
            </div>
            <!-- 用户名 -->
            <div class="art-nick-name">{{ author_data.nick_name }}</div>
            <!-- 用户等级 -->
            <div class="grade-name">菜鸡出道<span>0</span></div>
          </div>
          <!-- 右侧文本内容 -->
          <div class="art-con">
            <!-- 内容 -->
            <div class="con" v-html="author_data.content"></div>
            <!-- 发帖时间 -->
            <div class="art-time">{{ author_data.up_time }}-发帖</div>
          </div>
        </div>
        <!-- 回帖信息 -->
        <div class="reply-con-wrapper">
          <!-- 循环输出回帖 -->
          <ul class="reply-con" v-for="(r, index) in replyData" :key="r.id">
            <li class="reply">
              <!-- 左侧用户资料 -->
              <div class="rep-user">
                <!-- 楼层 -->
                <div class="Land2">{{ index + 2 }}楼</div>
                <div class="user-por">
                  <img
                    class="aut_por"
                    :src="getPortrait(r.portrait)"
                    alt="作者头像"
                    width="100"
                    height="100"
                  />
                </div>
                <!-- 用户名 -->
                <div class="art-nick-name">{{ r.nick_name }}</div>
                <!-- 用户等级 -->
                <div class="grade-name">菜鸡出道<span>0</span></div>
              </div>
              <!-- 右侧回帖内容 -->
              <div class="rep-con">
                <!-- 内容 -->
                <div class="con" v-html="r.reply_text"></div>
                <!-- 回帖时间 -->
                <div class="reply-time">
                  {{ r.updated_time.slice(0, 19) }}-回帖
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <!-- 发布回帖 -->
      <div class="post-reply-wrapper">
        <div class="post-wrapper">
          <!-- 小标题 -->
          <div class="post-title">
            <i class="el-icon-edit-outline"></i><span>发表回帖</span>
          </div>
          <!-- 提交按钮 -->
          <div class="post-btn">
            <el-button @click="postReply" class="but1" type="primary"
              >发表</el-button
            >
          </div>
        </div>

        <!-- 百度富文本编辑器 -->
        <div class="ueditor-wrapper">
          <vue-ueditor-wrap
            class="ueditor"
            v-model="replyText"
            :config="ueConfig"
          ></vue-ueditor-wrap>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import VueUeditorWrap from "vue-ueditor-wrap";

export default {
  name: "Article",
  components: {
    VueUeditorWrap,
  },
  data() {
    return {
      search_bar_data: "",
      // 作者的资料
      author_data: "",
      // 第一次获取资料
      firstExe: true,
      // 第一次进入刷新
      oneRefresh: true,
      replyText: "",
      // ueditor 设置信息
      ueConfig: {
        // 初始容器高度
        initialFrameHeight: 300,
        // 初始容器宽度
        initialFrameWidth: "800",
        // 上传文件接口
        enableAutoSave: false,
        elementPathEnable: false,
        wordCount: false,
        UEDITOR_HOME_URL: "/UEditor/",
        serverUrl: "http://localhost:8080/django/article/controller", // 上传文件接口
        toolbars: [
          [
            "undo", //撤销
            "bold", //加粗
            "indent", //首行缩进
            "italic", //斜体
            "underline", //下划线
            "strikethrough", //删除线
            "subscript", //下标
            "fontborder", //字符边框
            "superscript", //上标
            "formatmatch", //格式刷
            "fontfamily", //字体
            "fontsize", //字号
            "justifyleft", //居左对齐
            "justifycenter", //居中对齐
            "justifyright", //居右对齐
            "justifyjustify", //两端对齐
            "insertorderedlist", //有序列表
            "insertunorderedlist", //无序列表
            "lineheight", //行间距
            "simpleupload", //单图上传
            "insertimage", //多图上传
            "link", //超链接
            "insertvideo", //视频
          ],
        ],
      },
      replyData: "",
    };
  },
  watch: {
    // 当文章id发生改变时调用getArtcle获取新内容
    article_id() {
      if (this.article_id) {
        this.getArtcle();
      }
    },
  },
  computed: {
    article_id() {
      return this.$route.query.article_id;
    },
  },
  created() {
    this.oneGetArtcle();
    this.getReply();
  },
  methods: {
    // 获取回帖
    getReply() {
      // 请求服务器返回数据
      axios
        .get("/django/article/getReply", {
          params: {
            art_id: this.article_id,
          },
        })
        .then(
          (res) => {
            if (res.data["code"] === 200) {
              console.log(res.data);
              this.replyData = res.data["replyData"];
            } else if (res.data["code"] === 400) {
              console.log(res.data["message"]);
            }
          },
          (err) => {
            console.log(err.message);
          }
        );
    },
    // 发布回帖
    postReply() {
      // if (!sessionStorage.getItem('user_id')) {
      //     console.log(sessionStorage.getItem('user_id'))
      //     alert('未登录无法回帖')
      //     return
      // }
      // 设置csrf_token
      axios.get("http://localhost:8080/django/user/session").then((res) => {
        const csrf_token = res.data;
        window.sessionStorage.setItem("csrf_token", csrf_token);
      });
      //处理提交的数据
      let data = {
        art_id: this.article_id,
        replyText: this.replyText,
      };
      //上传回帖内容到服务器
      axios({
        method: "post",
        url: "http://localhost:8080/django/article/writeReply",
        data: data,
        headers: {
          //将csrf_token放在请求头中
          "X-CSRFToken": window.sessionStorage.getItem("csrf_token"),
        },
      }).then(
        (res) => {
          if (res.data["code"] === 400) {
            alert(res.data["message"]);
          } else if (res.data["code"] === 200) {
            alert(res.data["message"]);
            // this.$router.push({
            //     name: 'theme',
            //     query: {
            //         bar_id: this.$route.query.bar_id
            //     }
            // })
            // location.reload()
          }
        },
        (err) => {
          console.log(err.message);
        }
      );
    },
    // 如果头像图片没有信息就不返回图片地址
    getPortrait(url) {
      if (!url) {
        return url;
      } else if (url) {
        url = "/django/media/" + url;
        return url;
      }
    },
    // 获取文章内容
    getArtcle() {
      // console.log(this.article_id)
      axios
        .get("http://localhost:8080/django/article/getOneArticle", {
          params: {
            article_id: this.article_id,
          },
        })
        .then(
          (res) => {
            if (res.data["code"] === 200) {
              this.author_data = res.data;
              console.log(res.data);
            }
          },
          (err) => {
            console.log(err.message);
          }
        );
      this.firstExe = false;
    },
    // 创建页面时获取一次文章内容内容
    oneGetArtcle() {
      if (this.firstExe) {
        this.getArtcle();
      }
    },
  },
};
</script>

<style scoped>
* {
  font-family: "思源黑体R";
  color: #414157;
}

.Article {
  width: 1160px;
  height: 850px;
  background-color: white;
  border-radius: 5px;
}
/* 设置导航条 */
.bar-nav-wrapper {
  height: 72px;
  background-color: #414157;
  display: flex;
  justify-content: space-between;
  border-radius: 5px 5px 0 0;
}
/* 设置主题信息 */
.bar-info {
  display: flex;
  background-color: #fdde5e;
  margin-left: 10px;
}
/* 主题头像 */
.bar-por {
  width: 100px;
  height: 100px;
  border: 3px solid white;
  border-radius: 5px;
  box-sizing: border-box;
  position: relative;
  top: -28px;
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
}
.bar-por img {
  width: 100%;
  height: 100%;
}

/* 主题名 */
.bar-title-wrapper {
  margin: 10px 0 0 10px;
}
.bar-title span {
  font-size: 30px;
}
/* 关注按钮 */
.follow-but {
  background-color: #414157;
  color: white;
  border: none;
  width: 107px;
  height: 27px;
  position: relative;
  line-height: 6px;
  margin: 0 7px;
}

/* 简介 */
.bar-content {
  font-size: 20px;
  font-family: "思源黑体L";
  margin-top: 5px;
}
/* 设置导航栏 */
.article-nav {
  display: flex;
  font-size: 24px;
  align-items: center;
  height: 100%;
  margin-left: -137px;
}
.article-nav a {
  box-sizing: border-box;
  font-family: "思源黑体L";
  color: white;
  display: block;
  line-height: 46px;
  width: 154px;
  height: 46px;
  border-right: 1px solid rgba(255, 255, 255, 0.3);
  text-align: center;
}
.article-nav li:last-child a {
  border-right: 1px solid rgba(255, 255, 255, 0);
}
/* 经过效果 */
.article-nav a:hover {
  background-color: #fdde5e;
  height: 72px;
  line-height: 72px;
  border: 1px solid rgba(255, 255, 255, 0);
  color: #414157;
}
/* 设置搜索框 */
.search-bar {
  display: flex;
  align-items: center;
  margin-right: 30px;
}
/* 设置图标 */
.big-icon {
  margin-left: 10px;
}
/* 设置输入框 */
.search-bar .search-input {
  width: 170px;
  height: 30px;
}
/* 设置主体内容 */
.body-wrapper {
  height: 778px;
  overflow: auto;
}
/* 文章 */
/* 标题 */
.art-title-wrapper {
  display: flex;
  justify-content: space-between;
  height: 87px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.art-title-wrapper .art-title {
  font-size: 26px;
  font-family: "思源黑体L";
  line-height: 87px;
  margin-left: 10px;
}
/* 设置右侧功能 */
.art-title-btn {
  display: flex;
  margin-right: 24px;
  align-items: center;
}
.art-title-btn button {
  /* height: 23px; */
  padding: 6px 10px;
  border-color: #a0a0ab;
  margin-right: 10px;
}
/* 设置用户信息和文章内容 */
.atr-con-wrapper {
  position: relative;
  display: flex;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
/* 设置用户信息 */
.art-user {
  width: 190px;
  background-color: #cecedd;
  position: relative;
}
/* 楼层 */
.Land1 {
  background-color: #414157;
  color: #fdde5e;
  width: 50px;
  height: 26px;
  text-align: center;
  line-height: 26px;
  border-bottom-left-radius: 5px;
  position: absolute;
  right: 0;
  top: 0;
}

/* 头像 */
.user-por {
  width: 100px;
  height: 100px;
  margin: 0 auto;
  margin-top: 50px;
}
.user-por img {
  width: 100%;
  height: 100%;
  border-radius: 3px;
  border: 3px solid #fff;
  box-sizing: border-box;
}
/* 用户名 */
.art-nick-name {
  text-align: center;
  margin: 12px 0;
  font-size: 16px;
  font-family: "思源黑体L";
}
/* 等级 */
.grade-name {
  margin: 0 auto;
  text-align: center;
  width: 118px;
  height: 30px;
  background-image: linear-gradient(to bottom, #7a7a8e, #44445a, #414157);
  border-radius: 3px;
  color: #fff;
  line-height: 30px;
  margin-bottom: 30px;
}
.grade-name > span {
  width: 20px;
  height: 20px;
  display: inline-block;
  background-size: 20px;
  background-position: 0 0px;
  background-repeat: no-repeat;
  background-image: url("../static/等级图标.png");
  line-height: 20px;
  margin-left: 5px;
  color: #af7217;
}
/* 右侧内容 */
.art-con {
  box-sizing: border-box;
  width: 970px;
  padding: 35px 42px 18px 42px;
  /* position: relative; */
}
.con {
  font-size: 20px;
  font-family: "思源黑体L";
}
.art-time {
  position: absolute;
  bottom: 10px;
  right: 10px;
  color: #7e7e9c;
  font-family: "思源黑体L";
}
/* 设置回帖内容 */
.reply-con-wrapper {
}
.reply {
  display: flex;
  position: relative;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
.reply .rep-user {
  width: 190px;
  background-color: #cecedd;
  position: relative;
}
/* 2~楼 */
.Land2 {
  background-color: #414157;
  color: #fff;
  width: 50px;
  height: 26px;
  text-align: center;
  line-height: 26px;
  border-bottom-left-radius: 5px;
  position: absolute;
  right: 0;
  top: 0;
}
/* 右侧回帖内容 */
.rep-con {
  box-sizing: border-box;
  width: 970px;
  padding: 35px 42px 18px 42px;
}
.reply-time {
  position: absolute;
  bottom: 10px;
  right: 10px;
  color: #7e7e9c;
  font-family: "思源黑体L";
}
/* 发布回帖样式 */
.post-reply-wrapper {
  width: 1155px;
}
.post-title {
  font-size: 20px;
  margin: 20px 0;
}
/* 富文本编辑器 */
.ueditor-wrapper {
  width: 800px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 20px;
}
/* 按钮 */
.post-btn button {
  background-color: #414156;
  color: #fff;
  border: none;
  padding: 8px 30px;
  margin: 20px 0;
}
.post-wrapper{
    display: flex;
    align-items:center;
    justify-content:space-between;
    padding:0 175px;
}
</style>