<template>
    <div class="cp reg">
        <div class="userLogin">
            <h1 class="toLeft">欢迎注册</h1>
            <p class="loginBtn toLeft">已经有帐号
                <router-link to="login">登录</router-link>
            </p>
            <p>用户名<span class="split"></span>
                <el-input class="input" @focus="showTips" @blur="userIns" placeholder="请设置用户名"
                          v-model="username"></el-input>
            </p>
            <p v-show="userBool" class="Tips">此用户名太受欢迎了</p>
            <p>手机号<span class="split"></span>
                <el-input class="input" @blur="phoneIns" placeholder="可用于登录和找回密码" v-model="phone"></el-input>
            </p>
            <p v-show="phoneBool" class="Tips">这个手机号已经注册了</p>
            <p>密&nbsp;&nbsp;&nbsp;码<span class="split"></span>
                <el-input class="input" placeholder="请输入密码" v-model="password" show-password></el-input>
            </p>
            <p class="ver_text" v-show="verText">当前验证码为：{{verText}}</p>
            <p>验证码<span class="split"></span>
                <el-input class="input  ver_width" placeholder="请输入验证码" v-model="ver"></el-input>
                <span class="split"></span>
                <el-button :class="ver_style" @click.once="getVer">获取验证码</el-button>
            </p>
            <div class="but">
                <el-row>
                    <el-button @click="acc_post" class="input button" type="primary">注册</el-button>
                </el-row>
                <p class="agr"><input type="checkbox" v-model="agr"><a class="a_agr" :href="userAgr">《用户协议》</a></p>
            </div>
        </div>
        <p class="Tips_user" v-show="showT">设置后不可更改，中英文均可，最长14个英文或7个汉字</p>
        <router-link to="App"><img class="delete_ico" src="../static/x图标.png"></router-link>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Reg",
        data() {
            return {
                username: '',
                password: '',
                phone: '',
                ver: '',
                agr: false,
                userAgr: '',
                verText: '',
                userBool: false,
                phoneBool: false,
                showT: false,
                ver_style: 'ver_but2'
            }
        },
        methods: {
            showTips() {
                this.showT = true
            },
            //检查帐号是否存在
            userIns() {
                this.showT = false
                // console.log('userIns被触发')
                axios.get('http://localhost:8080/django/user/inspect?username=' + this.username).then(res => {
                    //处理回来的数据
                    if (res.data['userBool']) {
                        this.userBool = true
                    }
                    if (!res.data['userBool']) {
                        this.userBool = false
                    }
                }, err => {
                    console.log(err.message)
                })
            },
            //检查手机号是否存在
            phoneIns() {
                console.log('userIns被触发')
                axios.get('http://localhost:8080/django/user/inspect?phone=' + this.phone).then(res => {
                    //处理回来的数据
                    if (res.data['phoneBool']) {
                        this.phoneBool = true
                    }
                    if (!res.data['phoneBool']) {
                        this.phoneBool = false
                    }
                }, err => {
                    console.log(err.message)
                })
            },
            //获取验证码
            getVer() {
                this.verText = '666666'
                this.ver_style = "ver_but"
            },
            //注册帐号
            acc_post() {
                if (this.username.trim().length === 0) {
                    return alert('账号名不能为空')
                }
                if (this.phone.trim().length === 0) {
                    return alert('手机号不能为空')
                }
                if (this.password.trim().length === 0) {
                    return alert('密码不能为空')
                }
                if (this.ver.trim().length === 0) {
                    return alert('验证码不能为空')
                }
                //判断验证码是否正确
                if (this.ver !== this.verText) {
                    return alert('验证码不正确，请核对重试')
                }
                if (this.agr === false) {
                    return alert('请阅读并勾选用户协议')
                }
                if (this.userBool || this.phoneBool) {
                    return alert('资料填写不正确，请核实')
                }
                //提交的数据，直接提交对象会变成json字符串，需要后端解决
                const postData = {
                    username: this.username,
                    phone: this.phone,
                    password: this.password,
                    ver: this.ver
                }
                //通过get获取csrf_token值并保存
                axios.get('http://localhost:8080/django/user/login').then(res => {
                    const csrf_token = res.data
                    window.sessionStorage.setItem('csrf_token', csrf_token)
                })
                // post请求
                axios({
                    method: 'POST',
                    url: 'http://localhost:8080/django/user/reg',
                    data: {
                        data: postData
                    },
                    headers: {
                        //将csrf_token放在请求头中
                        'X-CSRFToken': window.sessionStorage.getItem("csrf_token")
                    }
                }).then((response) => {
                    alert(response.data)
                    this.$router.push({
                        name: 'login'
                    })
                }, (err) => {
                    console.log(err.message)
                })
            }
        },
        //路由生命周期钩子
        activated() {
            this.$bus.$emit('show_back', true)
        },
        deactivated() {
            this.$bus.$emit('show_back', false)
        }
    }
</script>

<style scoped>
    p {
        color: #262c3e;
    }

    .split {
        padding: 0 5px;
    }

    .input {
        width: 300px;
    }

    .reg {
        background-color: white;
        width: 640px;
        height: 650px;
        text-align: center;
        border-radius: 10px;
    }

    .button {
        border-radius: 10px;
        /*background-image: linear-gradient(to right, #00ff8d, #22ce7f);*/
        border-color: #fdde5e;
        background-color: #fdde5e;
        color: #262c3e;
        height: 60px;
        width: 270px;
        font-size: 28px;

    }

    .userLogin {
        position: relative;
        top: 10%;
    }

    .toLeft {
        font-size: 45px;
        color: #262c3e;
    }

    a {
        text-decoration: none;
    }

    .tail {
        background-color: #262c3e;
        height: 100px;
        position: relative;
        top: 50px;
    }

    .loginBtn {
        font-size: 14px;
        position: relative;
        top: -15px;
    }

    .agr {
        font-size: 14px;
    }

    .a_agr {
        text-decoration: none;
        color: cornflowerblue;
    }

    .but {
        position: relative;
        top: 20px;
    }

    .ver_width {
        width: 170px;
    }

    .ver_but {
        background-color: #414157;
        width: 120px;
        color: #b1b1b1;
    }

    .ver_but2 {
        background-color: #fdde5e;
        width: 120px;
        color: #262c3e;
    }

    .Tips {
        font-size: 12px;
        color: red;
    }

    .ver_text {
        font-size: 12px;
    }

    .Tips_user {
        background-color: #262c3e;
        color: white;
        padding: 3px 0;
        width: 370px;
        font-size: 14px;
        position: absolute;
        top: 172px;
        left: 140px;
        border-radius: 5px;
    }

    .delete_ico {
        position: absolute;
        top: 0px;
        left: 600px;
    }
</style>