<template>
  <div class="InfoInit info">
    <!-- 两个按钮 -->
    <div class="two-btn">
      <router-link to="login"
        ><p class="user_center user_init_color">点击登录</p></router-link
      >
      <router-link to="reg"
        ><p class="user_center user_init_color">点击注册</p></router-link
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "InfoInit",
  data() {
    return {
      user_center: "switch_color",
    };
  },
  methods: {},
};
</script>

<style scoped>
/* 整个大小 */
.InfoInit {
  width: 400px;
  height: 290px;
  background-color: #414157;
  color: #414157;
  font-family: "思源黑体R";
  font-size: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
/* 按钮样式 */
.user_center {
  padding: 10px;
  text-align: center;
  width: 100px;
  margin-top: 10px;
}
/* 默认样式 */
.user_init_color {
  background-color: white;
  border: solid 1px #414157;
  color: #414157;
  transition: background 0.2s, color 0.2s;
  -webkit-transition: background 0.2s, color 0.2s;
}
/* 经过样式 */
.user_init_color:hover {
  background-color: #fdde5e;
  border: solid 1px #414157;
  color: #414157;
}
</style>