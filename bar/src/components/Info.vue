<template>
  <div class="info">
    <!-- 整个部分 -->
    <div class="user-info">
      <!-- 用户数据 -->
      <div class="user-data-warpper">
        <div class="user-data">
          <!-- 用户头像 -->
          <div class="user-img">
            <img class="user-icon" :src="portrait" alt="头像" />
          </div>
          <!-- 头像右侧个人资料 -->
          <div class="user-info">
            <!-- 用户名 -->
            <div>
              <i class="fa fa-user"></i>
              <span class="user-nick-name"> {{ nick_name }}</span>
            </div>
            <!-- 等级 -->
            <div class="grade">
              等&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;级：<span class="grade-icon">{{
                expGrade
              }}</span>
            </div>
            <!-- 论坛币 -->
            <div class="m-cur-div">
              趣味币：<span class="m_cur">{{ bar_coin }}</span
              ><img src="../static/硬币图标.png" width="20" height="20" />
            </div>
            <!-- 设置个人信息按钮 -->
            <div class="set-info-wrapper">
              <el-row>
                <el-button class="set_info" type="info" plain @click="toInfoSet"
                  >设置个人资料</el-button
                >
              </el-row>
            </div>
          </div>
        </div>
      </div>

      <!-- 个人资料第二部分 -->
      <div class="user-data2">
        <!-- 排名 -->
        <div class="ranking">
          排名：001
          <div class="grade-name">
            <div class="g-name">菜鸡出道</div>
            <div class="g-img">{{ expGrade }}</div>
          </div>
        </div>
        <!-- 个人经验值 -->
        <div class="progressBar-u">
          <div class="exp-text">经验：</div>
          <!-- <el-progress
          class="progressBar"
          :text-inside="true"
          :stroke-width="22"
          :percentage="exp"
          status="exception"
        ></el-progress> -->
          <div class="exp-bar">
            <div class="bar-warpper">
              <div class="bar">
                <div class="bar-text">{{ exp }}/100</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "../static/css/components/Info.css";
export default {
  name: "Info",
  // data() {
  //     return {
  //         portrait: '/django/media/img/head_portrait/冒险岛头像.png'
  //     }
  // },
  computed: {
    expGrade() {
      let grade = this.exp / 100;
      return grade.toString().slice(0, 1);
    },
    username() {
      return this.$store.state.username;
    },
    exp: {
      get() {
        return this.$store.state.exp;
      },
      set(value) {
        this.$store.commit("Set_exp", value);
      },
    },
    nick_name: {
      get() {
        return this.$store.state.nick_name;
      },
      set(value) {
        this.$store.commit("Set_nick_name", value);
      },
    },
    age: {
      get() {
        return this.$store.state.age;
      },
      set(value) {
        this.$store.commit("Set_age", value);
      },
    },
    sex: {
      get() {
        return this.$store.state.sex;
      },
      set(value) {
        this.$store.commit("Set_sex", value);
      },
    },
    id_card: {
      get() {
        return this.$store.state.id_card;
      },
      set(value) {
        this.$store.commit("Set_id_card", value);
      },
    },
    bar_coin: {
      get() {
        return this.$store.state.bar_coin;
      },
      set(value) {
        this.$store.commit("Set_bar_coin", value);
      },
    },
    portrait: {
      // eslint-disable-next-line vue/return-in-computed-property
      get() {
        if (!this.$store.state.portrait) {
          return "";
        } else if (this.$store.state.portrait) {
          let src = "/django/media/" + this.$store.state.portrait;
          // let src = this.$store.state.portrait
          return src;
        }
      },
      set(value) {
        this.$store.commit("Set_portrait", value);
      },
    },
  },
  methods: {
    // 图片链接替换为可用链接
    urls(url) {
      return "/django/media/" + url;
    },
    toInfoSet() {
      this.$router.push({
        name: "info_set",
      });
    },
  },
};
</script>

<style scoped>
/* .info {
  width: 400px;
  height: 290px;
  background-color: white;
  color: #414157;
}

* {
  padding: 0;
  margin: 0;
  font-family: 思源黑体R;
  font-size: 20px;
}

.set_info {
  position: relative;
  font-size: 12px;
  padding: 4px;
  left: 130px;
  top: -150px;
}

.user_icon {
  position: absolute;
  top: -120px;
  border-radius: 5px;
  border: solid 3px white;
  box-shadow: 2px 2px 3px rgba(0, 0, 0, 0.3);
}

.Grade_icon {
  background-image: url("../static/等级图标.png");
  background-size: 30px;
  background-repeat: no-repeat;
  padding: 5px 10px 10px 10px;
  color: #bb8738;
  text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.3);
}

.info_u {
  position: relative;
  top: -95px;
  left: 135px;
}

.u_logo_icon {
  position: relative;
  top: -15px;
}

.m_cur {
  color: #f33670;
}

.user_data {
  position: relative;
  left: 50%;
  margin-left: -150px;
  top: 180px;
}

.Grade_name {
  background-color: #414157;
  padding: 7px 40px 7px 20px;
  color: white;
  border-radius: 3px;
  background-image: linear-gradient(#7a7a8e, #414157);
}

.Grade2 {
  font-size: 16px;
  position: relative;
  left: -35px;
  background-image: url("../static/等级图标.png");
  background-size: 25px;
  background-repeat: no-repeat;
  padding: 4px 10px 5px 8px;
  color: #bb8738;
  text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.3);
  top: -2px;
}

.progressBar {
  width: 200px;
  position: relative;
  top: -28px;
  left: 60px;
}

.user_data2 {
  position: relative;
  left: 50%;
  margin-left: -145px;
  top: 90px;
}

.progressBar_u {
  padding: 10px 0px;
} */
</style>