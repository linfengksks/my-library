<template>
  <div class="Home">
    <!-- 首页主DIV -->
    <div class="ConDisplay">
      <!-- 头部导航 -->
      <div class="top-nav">
        <Title />
      </div>

      <!-- 内容部分 -->
      <div class="div-body">
        <!-- 左侧部分 -->
        <div class="left-bar">
          <ThemeInit />
        </div>
        <!-- 右侧部分 -->
        <div class="right-bar">
          <Info v-show="username"></Info>
          <InfoInit v-show="!username"></InfoInit>
          <MoreInfo></MoreInfo>
        </div>
      </div>

      <!-- 弹出层 -->
      <div class="eject-bar">
        <div v-show="show_hidden_back" class="hidden_back"></div>
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </div>
    </div>
  </div>
</template>

<script>
import Title from "../components/Title";
import MoreInfo from "../components/MoreInfo";
import ThemeInit from "../components/ThemeInit";
import InfoInit from "../components/InfoInit";
import axios from "axios";
import Info from "../components/Info";

export default {
  name: "Home",
  components: {
    Info,
    Title,
    MoreInfo,
    ThemeInit,
    InfoInit,
  },
  data() {
    return {
      show_hidden_back: false,
      username: "",
    };
  },
  methods: {
    show_back(data) {
      this.show_hidden_back = data;
    },

    readData() {
      //通过get获取csrf_token值并保存
      axios.get("http://localhost:8080/django/user/session").then(
        (res) => {
          this.username = res.data["username"];
          this.$store.commit("SetUserName", this.username);
          this.$store.commit("Set_nick_name", res.data["nick_name"]);
          this.$store.commit("Set_sex", res.data["sex"]);
          this.$store.commit("Set_age", res.data["age"]);
          this.$store.commit("Set_id_card", res.data["id_card"]);
          this.$store.commit("Set_bar_coin", res.data["bar_coin"]);
          this.$store.commit("Set_exp", res.data["exp"]);
          this.$store.commit("Set_portrait", res.data["portrait"]);
        },
        (err) => {
          console.log(err.message);
        }
      );
    },
  },
  mounted() {
    this.$bus.$on("show_back", this.show_back);
    this.readData();
  },
};
</script>

<style scoped>
/* 注册字体 */
@font-face {
  font-family: "思源黑体B";
  src: url("../static/字体/SourceHanSansCN-Bold.otf");
}
/* 整个背景 */
.Home {
  width: 1920px;
  height: 1080px;
  background-image: url("../static/背景.jpg");
}
/* 内容部分 */
.ConDisplay {
  width: 1600px;
  height: 1030px;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  margin: 0 auto;
  position: relative;
  top: 15px;
}
/* 内容部分 */
.div-body {
  display: flex;
  margin-top: 67px;
  justify-content: space-evenly;
}
/* 左侧部分 */
.left-bor {
  position: relative;
}
/* 右侧部分 */
.right-bor {
  height: 850px;
  display: flex;
  flex-direction: column;
  justify-content: start;
  overflow: hidden;
}
/* 默认登录框 */
.InfoInit {
  /* margin-top: -16px; */
}
/* 更多主题 */
.MoreInfo {
  margin-top: 15px;
}
/* 弹出层脱离文档流 */
/* .eject-bar {
  width: 100%;
  height: 100%;
  position: relative;
  left: 0;
  top: 0;
} */
/* 定位 */
.eject {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: auto;
}
/* 弹出层的黑背景 */
.hidden_back {
  position: absolute;
  left: -160px;
  top: -15px;
  /* margin: auto; */
  width: 1920px;
  height: 1080px;
  background-color: rgba(0, 0, 0, 0.3);
}

/* 弹出层的样式 */
.InfoSet{
  position: absolute;
  left: 13px;
  top: 167px;
}
</style>