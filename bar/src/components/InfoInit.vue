<template>
    <div class="InfoInit info">
        <router-link to="login"><p class="user_center user_init_color">点击登录</p></router-link>
        <router-link to="reg"><p class="user_center user_init_color">点击注册</p></router-link>
    </div>
</template>

<script>
    export default {
        name: "InfoInit",
        data() {
            return {
                user_center: 'switch_color',
            }
        },
        methods: {}
    }
</script>

<style scoped>
    a{
        text-decoration: none;
    }
    .InfoInit {
        width: 400px;
        height: 290px;
        background-color: #414157;
        color: #414157;
    }

    * {
        padding: 0;
        margin: 0;
        font-family: 思源黑体R;
        font-size: 20px;
    }

    .user_center {
        padding: 10px;
        text-align: center;
        width: 100px;
        margin: 15px auto;
        position: relative;
        top: 70px;
    }

    .user_init_color {
        background-color: white;
        border: solid 1px #414157;
        color: #414157;
        transition: background 0.2s, color 0.2s;
        -webkit-transition: background 0.2s, color 0.2s;
    }

    .user_init_color:hover {
        background-color: #fdde5e;
        border: solid 1px #414157;
        color: #414157;
    }
</style>