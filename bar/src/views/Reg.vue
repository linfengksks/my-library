<template>
  <div class="eject reg">
    <div class="userLogin">
      <!-- 标题 -->
      <h1 class="reg-title">欢迎注册</h1>
      <!-- 提示有帐号登录 -->
      <div class="reg-mini-title">
        已经有帐号
        <router-link to="login">登录</router-link>
      </div>
      <!-- 注册信息 -->
      <div class="reg-data">
        <!-- 用户名外框 -->
        <div class="username-wrapper">
          <!-- 用户名 -->
          <div class="username">
            <span class="input-text">用&nbsp;&nbsp;户&nbsp;&nbsp;名</span>
          </div>
          <!-- 用户名输入框 -->
          <div class="username-input">
            <el-input
              class="input"
              @focus="showTips"
              @blur="userIns"
              placeholder="请设置用户名"
              v-model="username"
            ></el-input>
            <p v-show="userBool" class="Tips">此用户名太受欢迎了</p>
            <!-- 提示 -->
            <div class="Tips-user" v-show="showT">
              <!-- <p class="Tips-user" > -->
              设置后不可更改，中英文均可，最长14个英文或7个汉字
              <div class="triangle"></div>
            </div>
          </div>
        </div>
        <!-- 手机号外框 -->
        <div class="phone-wrapper">
          <!-- 手机号 -->
          <div class="phone">
            <span class="input-text"> 手&nbsp;&nbsp;机&nbsp;&nbsp;号</span>
          </div>
          <!-- 手机号输入框 -->
          <div class="phone-input">
            <el-input
              class="input"
              @blur="phoneIns"
              placeholder="可用于登录和找回密码"
              v-model="phone"
            ></el-input>
            <p v-show="phoneBool" class="Tips">这个手机号已经注册了</p>
          </div>
        </div>
        <!-- 密码外框 -->
        <div class="pwd-wrapper">
          <div class="pwd">
            <span class="input-text">
              密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码</span
            >
          </div>
          <!-- 密码输入框 -->
          <div class="pwd-input">
            <el-input
              class="input"
              placeholder="请输入密码"
              v-model="password"
              show-password
              @blur="pwd_tips_test()"
            ></el-input>
            <p class="Tips" v-show="pwd_tips">请输入密码</p>
          </div>
        </div>
        <!-- 确认密码外框 -->
        <div class="pwd2-wrapper">
          <!-- 确认密码 -->
          <div class="pwd2">
            <span class="input-text"> 确认密码</span>
          </div>
          <!-- 确认密码输入框 -->
          <div class="pwd2-input">
            <el-input
              class="input"
              placeholder="请再次输入密码"
              v-model="password2"
              show-password
              @blur="pwd2_tips_test()"
            ></el-input>
            <p v-show="pwd2_tips" class="Tips">
              两次输入的密码不一致，请确认下
            </p>
          </div>
        </div>
        <!-- 验证码外框 -->
        <div class="ver-text-wrapper">
          <!-- 验证密码 -->
          <div class="ver">
            <span class="input-text">验&nbsp;&nbsp;证&nbsp;&nbsp;码</span>
          </div>
          <!-- 验证码密码输入框 -->
          <div class="ver-input">
            <p class="ver_text" v-show="verText">当前验证码为：{{ verText }}</p>

            <el-input
              class="input ver_width"
              placeholder="请输入验证码"
              v-model="ver"
            ></el-input>
            <!-- 获取密码按钮 -->
            <el-button class="ver-btn" @click.once="getVer"
              >获取验证码</el-button
            >
          </div>
        </div>
      </div>
      <!-- 注册按钮 -->
      <div class="but">
        <el-row>
          <el-button @click="acc_post" class="button" type="primary"
            >注册</el-button
          >
        </el-row>
        <!-- 用户协议 -->
        <p class="agr">
          <input type="checkbox" v-model="agr" /><a
            class="a_agr"
            :href="userAgr"
            >《用户协议》</a
          >
        </p>
      </div>
    </div>
    <router-link to="App"
      ><img class="sign-out-ico" src="../static/x图标.png"
    /></router-link>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Reg",
  data() {
    return {
      username: "",
      password: "",
      password2: "",
      phone: "",
      ver: "",
      agr: false,
      userAgr: "",
      verText: "",
      userBool: false,
      phoneBool: false,
      showT: false,
      ver_style: "ver_but2",
      // 用户未输入密码时提示
      pwd_tips: false,
      // 两次密码是否一致
      pwd2_tips: false,
    };
  },
  methods: {
    // 检验用户密码两次输入是否一致
    pwd2_tips_test() {
      console.log("重复密码验证");
      // 如果两次密码不一致
      if (this.password != this.password2) {
        this.pwd2_tips = true;
      }
      // 如果一致
      if (this.password === this.password2) {
        this.pwd2_tips = false;
      }
    },
    // 检验用户是否输入了密码
    pwd_tips_test() {
      // 如果当前用户密码不存在就提示，
      if (!this.password) {
        this.pwd_tips = true;
      }
      // 如果输入了密码就不提示了
      if (this.password) {
        this.pwd_tips = false;
      }
    },
    showTips() {
      this.showT = true;
    },
    //检查帐号是否存在
    userIns() {
      this.showT = false;
      // console.log('userIns被触发')
      axios
        .get(
          "http://localhost:8080/django/user/inspect?username=" + this.username
        )
        .then(
          (res) => {
            //处理回来的数据
            if (res.data["userBool"]) {
              this.userBool = true;
            }
            if (!res.data["userBool"]) {
              this.userBool = false;
            }
          },
          (err) => {
            console.log(err.message);
          }
        );
    },
    //检查手机号是否存在
    phoneIns() {
      console.log("userIns被触发");
      axios
        .get("http://localhost:8080/django/user/inspect?phone=" + this.phone)
        .then(
          (res) => {
            //处理回来的数据
            if (res.data["phoneBool"]) {
              this.phoneBool = true;
            }
            if (!res.data["phoneBool"]) {
              this.phoneBool = false;
            }
          },
          (err) => {
            console.log(err.message);
          }
        );
    },
    //获取验证码
    getVer() {
      this.verText = "666666";
      this.ver_style = "ver_but";
    },
    //注册帐号
    acc_post() {
      if (this.username.trim().length === 0) {
        return alert("账号名不能为空");
      }
      if (this.phone.trim().length === 0) {
        return alert("手机号不能为空");
      }
      if (this.password.trim().length === 0) {
        return alert("密码不能为空");
      }
      if (this.ver.trim().length === 0) {
        return alert("验证码不能为空");
      }
      //判断验证码是否正确
      if (this.ver !== this.verText) {
        return alert("验证码不正确，请核对重试");
      }
      if (this.agr === false) {
        return alert("请阅读并勾选用户协议");
      }
      if (this.userBool || this.phoneBool) {
        return alert("资料填写不正确，请核实");
      }
      //提交的数据，直接提交对象会变成json字符串，需要后端解决
      const postData = {
        username: this.username,
        phone: this.phone,
        password: this.password,
        ver: this.ver,
      };
      //通过get获取csrf_token值并保存
      axios.get("http://localhost:8080/django/user/login").then((res) => {
        const csrf_token = res.data;
        window.sessionStorage.setItem("csrf_token", csrf_token);
      });
      // post请求
      axios({
        method: "POST",
        url: "http://localhost:8080/django/user/reg",
        data: {
          data: postData,
        },
        headers: {
          //将csrf_token放在请求头中
          "X-CSRFToken": window.sessionStorage.getItem("csrf_token"),
        },
      }).then(
        (response) => {
          alert(response.data);
          this.$router.push({
            name: "login",
          });
        },
        (err) => {
          console.log(err.message);
        }
      );
    },
  },
  //路由生命周期钩子
  activated() {
    this.$bus.$emit("show_back", true);
  },
  deactivated() {
    this.$bus.$emit("show_back", false);
  },
};
</script>

<style scoped>
/* 设置整个大小 */
.reg {
  background-color: white;
  width: 640px;
  height: 650px;
  text-align: center;
  border-radius: 10px;
  color: #414157;
  font-family: "思源黑体R";
}
/* 标题 */
.reg-title {
  margin-top: 48px;
  font-size: 45px;
  font-family: "思源黑体B";
}
/*小标题  */
.reg-mini-title {
  margin: 15px 0 55px 0;
  font-size: 18px;
  color: #898989;
}
/* 登录链接 */
.reg-mini-title a {
  color: #3a3a7a;
}

/* 设置用户名等文字 */
.input-text {
  font-size: 26px;
}
/* 用户名下面的提示 */
.Tips-user {
  width: 317px;
  height: 30px;
  background-color: #414157;
  border-radius: 5px;
  color: white;
  font-size: 12px;
  line-height: 30px;
  text-align: center;
  position: absolute;
  left: 0;
  right: 0;
  margin: 0 auto;
  top: -40px;
}
/* 设置下方三角符号 */
.triangle {
  width: 0;
  height: 0;
  /* background-color: red; */
  border: 6px solid transparent;
  border-top-color: #414157;
  margin: 0 auto;
}
/* 以输入框外框定位 */
.username-input {
  position: relative;
}
/* 输入框 */
.input {
  width: 360px;
  margin-left: 10px;
}
.reg-data {
  width: 480px;
  height: 300px;
  display: flex;
  flex-direction: column;
  /* align-content: space-between; */
  justify-content: space-between;
  /* align-items: center; */
  /* border: 1px solid springgreen; */
  margin: 0 auto;
  text-align: left;
}
/* 输入框定位 */
.reg-data > div {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
/* 单独设置验证码输入框 */
.ver-input .input {
  width: 238px;
  /* 添加空隙 */
  margin-right: 10px;
}
/* 获取验证码按钮 */
.el-button {
  background-color: #fdde5e;
  color: #414157;
  border: none;
}
/* 经过效果 */
.el-button:hover {
  background-color: #ebc945;
}
/* 退出按钮 */
.sign-out-ico {
  position: absolute;
  right: -1px;
  top: -1px;
}
/* 注册按钮 */
.but {
  margin: 27px 0;
}
.but button {
  width: 200px;
  height: 50px;
  font-size: 28px;
}

.but > p {
  margin-top: 27px;
}
/* 设置提示语 */
.Tips {
  font-size: 12px;
  color: red;
  margin-left: 10px;
  margin-top: 5px;
  position: absolute;
}
/* 设置验证码 */
.ver_text {
  font-size: 12px;
  position: absolute;
  margin-left: 60px;
  margin-top: -18px;
}
.ver-input {
  position: relative;
}
</style>