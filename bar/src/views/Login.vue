<template>
    <div class="cp login">
        <div class="userLogin">
            <p class="title">用户名密码登录</p>
            <p><input @keydown.enter="acc_post" @blur="testing_user" class="input_text inp_user" type="text"
                      placeholder="手机号/用户名/邮箱"
                      v-model="username"></p>

            <p><input @keydown.enter="acc_post" @blur="testing_pwd" class="input_text inp_pwd" type="password"
                      placeholder="请输入密码"
                      v-model="password"></p>


            <!--            <el-input class="input_text" placeholder="手机号/用户名/邮箱" v-model="username"></el-input>-->
            <!--            <el-input class="input_text" placeholder="请输入密码" v-model="password" show-password></el-input>-->

            <el-row>
                <el-button @click="acc_post" class="input button" type="primary">登录</el-button>
            </el-row>
            <p v-show="testing_u" class="testing user">用户名不能为空</p>
            <p v-show="testing_p" class="testing pwd">密码不能为空</p>
            <p><a class="pwdRetrieve" href="https://www.baidu.com">忘记密码？</a></p>
            <router-link class="reg_text" to="reg">去注册</router-link>
            <router-link to="App"><img class="delete_ico" src="../static/x图标.png"></router-link>

        </div>
    </div>

</template>

<script>
    import axios from 'axios'

    export default {
        name: "Login",
        data() {
            return {
                username: '',
                password: '',
                testing_u: false,
                testing_p: false,
            }
        },
        methods: {
            //检测用户输入框是否为空
            testing_user() {
                if (!this.username) {
                    this.testing_u = true
                } else {
                    this.testing_u = false
                }
            },
            //检测密码输入框是否为空
            testing_pwd() {
                if (!this.password) {
                    this.testing_p = true
                } else {
                    this.testing_p = false
                }
            },
            acc_post() {
                if (this.username.trim().length === 0) {
                    return alert('账号名不能为空')
                }
                if (this.password.trim().length === 0) {
                    return alert('密码不能为空')
                }
                //提交的数据，直接提交对象会变成json字符串，需要后端解决
                const postData = {
                    username: this.username,
                    password: this.password
                }
                //通过get获取csrf_token值并保存
                axios.get('http://localhost:8080/django/user/login').then(res => {
                    const csrf_token = res.data
                    window.sessionStorage.setItem('csrf_token', csrf_token)
                })
                // post请求
                axios({
                    method: 'POST',
                    url: 'http://localhost:8080/django/user/login',
                    data: {
                        data: postData
                    },
                    headers: {
                        //将csrf_token放在请求头中
                        'X-CSRFToken': window.sessionStorage.getItem("csrf_token")
                    }
                }).then((res) => {
                    // if (res.data['username']) {
                    //     sessionStorage.setItem('username', res.data['username'])
                    //     sessionStorage.setItem('username_card', res.data['username_card'])
                    //     alert('登录成功')
                    //     this.$router.push({
                    //         name: 'App'
                    //     })
                    //如果返回回来的状态为400，提示密码用户错误
                    if (res.data['code'] === 400) {
                        alert('用户名或密码错误')
                    }
                    if (res.data['code'] === 200) {
                        alert('登录成功')
                        this.$router.push({
                            name: 'app',
                            params: {
                                id: 1
                            }
                        })
                        location. reload()
                    }
                }, (err) => {
                    console.log(err.message)
                    alert(err.message)
                })
            }
        },
        // watch: {
        //     $route(to, from) {
        //         this.$router.go(0)
        //     }
        // },
        //路由生命周期钩子
        // mounted() {
        //     console.log('login 激活了')
        //     this.$bus.$emit('show_back','1')
        // },
        // beforeDestroy() {
        //     console.log('login 被销毁了')
        //     this.$bus.$emit('show_back','0')
        // }
        activated() {
            this.$bus.$emit('show_back', true)
        },
        deactivated() {
            this.$bus.$emit('show_back', false)
        }
    }
</script>

<style scoped>
    @font-face {
        font-family: "思源黑体L";
        src: url("../static/字体/SourceHanSansCN-Light.otf");
    }

    @font-face {
        font-family: 思源黑体R;
        src: url("../static/字体/SourceHanSansCN-Regular.otf");
    }

    .login {
        background-color: white;
        width: 640px;
        height: 430px;
        text-align: center;
        border-radius: 10px;
    }

    .button {
        border-radius: 10px;
        /*background-image: linear-gradient(to right, #00ff8d, #22ce7f);*/
        border-color: #fdde5e;
        background-color: #fdde5e;
        color: #262c3e;
        width: 278px;
        height: 50px;
        font-family: 思源黑体R;
        font-size: 22px;
        position: relative;
        top: 15px;
    }

    .userLogin {
        position: relative;
        top: 10%;
    }

    .title {
        font-size: 30px;
        padding: 10px 0;
        color: #414157;
    }

    a {
        text-decoration: none;
    }


    .input_text {
        width: 380px;
        height: 48px;
        font-size: 20px;
        border-radius: 8px;
        border: solid #c8c8c8 1px;
        padding: 0 20px;
        font-family: 思源黑体L;
        margin: 15px 0;
        position: relative;
        top: -10px;
    }

    .reg_text {
        position: absolute;
        color: #b2b6ba;
        font-size: 14px;
        left: 480px;
        top: 145px;
        padding: 5px 0;
    }

    .pwdRetrieve {
        position: absolute;
        color: #b2b6ba;
        font-size: 14px;
        left: 470px;
        top: 242px;
        padding: 5px 0;
    }

    .testing {
        color: red;
        font-size: 14px;
    }

    .user {
        position: absolute;
        top: 130px;
        left: 115px;

    }

    .pwd {
        position: absolute;
        text-align: left;
        top: 230px;
        left: 115px;
    }

    .delete_ico {
        position: relative;
        float: right;
        top: -421px;
    }
</style>