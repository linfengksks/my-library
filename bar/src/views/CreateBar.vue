<template>
    <div class="CreateBar Theme">
        <div class="createBody">
            {{getUserData()}}
            <p class="title">创建主题吧</p>
            <p>主题名
                <el-input class='bar_input' placeholder="请输入昵称" v-model="bar_name"
                          clearable></el-input>
            </p>
            <p>用户名
                <el-input class='bar_input' placeholder="请输入昵称" v-model="username"
                          clearable disabled></el-input>
            </p>
            <p>身份证
                <el-input class='bar_input' placeholder="请输入昵称" v-model="userData.id_card"
                          clearable disabled></el-input>
            </p>
            <p>简&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;介
                <el-input class='bar_input'
                          type="textarea"
                          :rows="2"
                          placeholder="请输入内容"
                          v-model="int">
                </el-input>
            </p>
            <el-button @click="createBar" class="setBut" type="primary">申请</el-button>
            <el-button @click='re_app' class="setBut" type="primary">返回</el-button>

        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "CreateBar",
        data() {
            return {
                bar_name: '',
                id_card: '',
                int: '',
                userData: '',
                firstGetUserData: true,
            }
        },
        computed: {
            username() {
                return this.$store.state.username
            }
        },
        methods: {
            // 获取用户的身份证
            getUserData() {
                // 只获取一次
                if (this.firstGetUserData === true) {
                    // 向服务器获取当前用户信息
                    axios.get('http://localhost:8080/django/user/getUserData').then(
                        res => {
                            if (res.data['code'] === 200) {
                                this.userData = res.data
                                console.log(res.data['message'])
                            } else if (res.data['code'] === 400) {
                                alert(res.data['message'])
                                this.$router.push({
                                    name: 'app'
                                })
                            }
                            this.firstGetUserData = false
                        }, err => {
                            console.log(err.message)
                        }
                    )
                }

            },
            // 返回主页
            re_app() {
                this.$router.push({
                    name: 'app'
                })
            },
            // 创建贴吧
            createBar() {
                // 创建提交的资料
                let data = {
                    bar_name: this.bar_name,
                    username: this.username,
                    id_card: this.id_card,
                    int: this.int
                }
                // 请求服务器创建吧
                axios.get('http://localhost:8080/django/article/createBar', {
                    params: {
                        data
                    }
                }).then(res => {
                    alert(res.data['message'])
                }, err => {
                    console.log(err.message)
                })

            }
        }
    }
</script>

<style scoped>
    * {
        font-family: 思源黑体R;
        color: #414157;
        text-align: center;
    }

    .CreateBar {
        width: 1160px;
        height: 850px;
        background-color: white;
        border-radius: 5px;
    }

    .title {
        font-size: 30px;
        text-align: center;
    }

    .bar_input {
        width: 300px;
        padding: 0 5px;
    }

    .setBut {
        background-color: #262c3e;
        color: white;
        border-color: #414157;
    }

    .setBut:hover {
        background-color: #414157;
    }

    .createBody {
        position: relative;
        top: 150px;
    }
</style>