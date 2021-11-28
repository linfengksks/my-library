<template>
  <div class="Title">
    <!-- 左侧LOGO部分 -->
    <div class="left-logo">
      <!-- 主页LOGO -->
      <div class="logo-wrapper">
        <img class="logo" src="../static/LOGOlunx160.png" width="160px" />
      </div>
      <!-- 搜索框 -->
      <div class="search-bar">
        <!-- 搜索框 -->
        <div class="search-input">
          <el-input
            @keydown.enter.native="search_bar" class="search_input"
            placeholder="请输入内容" v-model="search_data" clearable>
          </el-input>
        </div>
        <!-- 搜索按钮 -->
        <div class="search-but">
          <el-button class="s_btn1" type="primary" @click="toBar"
            >进入主题</el-button
          >
          <el-button @click="search_bar" class="s_btn2" type="primary"
            >全论坛搜索</el-button
          >
        </div>
      </div>
    </div>
    <!-- 右侧导航条 -->
    <div class="right-nav">
      <!-- 导航条 -->
      <ul class="top-nav">
        <li>
          <i class="fa fa-diamond" aria-hidden="true"></i><a href="/">视趣首页</a>
        </li>
        <li v-show="!username">
          <i class="fa fa-sign-in" aria-hidden="true"></i><router-link to="login">登录</router-link>
        </li>
        <li v-show="!username">
          <i class="fa fa-user-plus"></i><router-link to="reg">注册</router-link>
        </li>
        <li v-show="username">
          <a href="#">嗨！{{ username }}</a>
        </li>
        <li v-show="username">
          <i class="fa fa-mail-reply"></i><a href="" @click="signOut">注销</a>
        </li>
        <li>
          <i class="fa fa-newspaper-o"></i><a href="#">匿名浏览</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// 引入css
import "../static/css/components/Title.css";
export default {
  name: "Title",
  data() {
    return {
      search_data: "",
      home: "http://localhost:8080/#/",
      bar_id: "",
    };
  },
  computed: {
    username() {
      return this.$store.state.username;
    },
  },
  methods: {
    // 点击进入主题
    toBar() {
      axios
        .get("/django/article/search_bar", {
          params: {
            seachData: this.search_data,
          },
        })
        .then(
          (res) => {
            if (res.data["code"] === 200) {
              res.data["bar_data"].forEach((bar) => {
                if (bar.bar_name === this.search_data) {
                  this.$router.push({
                    name: "theme",
                    query: {
                      bar_id: bar.id,
                      times: new Date(),
                    },
                  });
                } else {
                  alert("主题名需要完全一致，请使用旁边的全论坛搜索");
                }
              });
            } else if (res.data["code"] === 400) {
              alert(res.data["message"]);
            }
          },
          (err) => {
            console.log(err.message);
          }
        );
    },
    // 搜索主题和文章
    search_bar() {
      axios
        .get("/django/article/search_bar", {
          params: {
            seachData: this.search_data,
          },
        })
        .then(
          (res) => {
            if (res.data["code"] === 200) {
              this.$store.state.resultData = res.data;
              console.log(">>>>>", res.data);
              console.log(res.data["message"]);
              this.$router.push({
                name: "search",
              });
            } else if (res.data["code"] === 400) {
              alert(res.data["message"]);
            }
          },
          (err) => {
            console.log(err.message);
          }
        );
    },
    signOut() {
      //    跨域请求，上传注销信息
      axios
        .get("http://localhost:8080/django/user/session", {
          params: {
            pattern: "delete",
            username: this.username,
          },
        })
        .then(
          (res) => {
            if (res.data["code"] === 200) {
              alert("注销成功");
              this.$router.push({
                name: "title",
                params: {
                  id: 1,
                },
              });
            }
          },
          (err) => {
            console.log(err.message);
          }
        );
    },
  },
};
</script>

<style scoped>
/* @font-face {
  font-family: "思源黑体R";
  src: url("../static/字体/SourceHanSansCN-Regular.otf");
}

a {
  text-decoration: none;
  color: black;
}

.content {
  width: 1600px;
  height: 100px;
  background-color: white;
  position: relative;
  border-radius: 10px 10px 0 0;
  top: 10px;
  margin: 0 auto;
  box-shadow: 0px 4px 3px rgba(0, 0, 0, 0.3);
}

.logo {
  position: relative;
  top: -30px;
  left: 80px;
}

.title {
  color: #414157;
  float: right;
  font-family: "思源黑体R";
  font-size: 20px;
  position: relative;
  left: -30px;
  top: 20px;
}

.title li {
  display: inline;
  padding: 0 45px;
}

.title a {
  color: #414157;
}

.title_icon {
  padding: 3px 10px;
}

.search_input {
  width: 244px;
  position: absolute;
  top: 30px;
  left: 260px;
}

.search_but {
  position: absolute;
  top: 39px;
  left: 500px;
}

.s_but1 {
  background-color: #fdde5e;
  color: #262c3e;
  padding: 12px 10px;
  position: relative;
  border-radius: 0;
  top: -9px;
  border-color: #fdde5e;
}

.s_but2 {
  background-color: #262c3e;
  color: #fdde5e;
  padding: 12px 10px;
  border-radius: 0 5px 5px 0;
  position: relative;
  left: -13px;
  top: -9px;
  border-color: #262c3e;
} */

/*.cp {*/
/*    margin: 0 auto;*/
/*    position: relative;*/
/*    top: 0px;*/
/*}*/
</style>