<template>
    <div class="bg">
        <Title/>
        <div class="ConDisplay">
        </div>
        <ThemeInit/>
        <!--        <Theme/>-->
        <Info v-show="username"></Info>
        <InfoInit v-show="!username"></InfoInit>
        <MoreInfo></MoreInfo>
        <p v-show="show_hidden_back" class="hidden_back"></p>
        <keep-alive>
            <router-view></router-view>
        </keep-alive>

    </div>
</template>

<script>
    import Title from "../components/Title";
    import MoreInfo from '../components/MoreInfo'
    import ThemeInit from '../components/ThemeInit'
    import InfoInit from '../components/InfoInit'
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
                username: '',
            }
        },
        methods: {
            show_back(data) {
                this.show_hidden_back = data
            },

            readData() {
                //通过get获取csrf_token值并保存
                axios.get('http://localhost:8080/django/user/session').then(res => {
                    this.username = res.data['username']
                    this.$store.commit('SetUserName', this.username)
                    this.$store.commit('Set_nick_name', res.data['nick_name'])
                    this.$store.commit('Set_sex', res.data['sex'])
                    this.$store.commit('Set_age', res.data['age'])
                    this.$store.commit('Set_id_card', res.data['id_card'])
                    this.$store.commit('Set_bar_coin', res.data['bar_coin'])
                    this.$store.commit('Set_exp', res.data['exp'])
                    this.$store.commit('Set_portrait', res.data['portrait'])
                }, err => {
                    console.log(err.message)
                })
            }
        },
        mounted() {
            this.$bus.$on('show_back', this.show_back)
            this.readData()
        },

    }
</script>

<style scoped>
    .bg {
        width: 1920px;
        height: 1080px;
        background-image: url("../static/背景.jpg");
    }

    .content {
        /*position: absolute;*/
        /*left: 50%;*/
        /*margin-left: -784px;*/
        /*top: 20px;*/
    }

    .ConDisplay {
        width: 1600px;
        height: 960px;
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 0 0 10px 10px;
    }

    .ConDisplay {
        margin: 0 auto;
        position: relative;
        top: 0px;
    }

    .Theme {
        position: absolute;
        top: 180px;
        left: 180px;
    }

    .cp {
        position: absolute;
        margin: auto;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
    }

    .hidden_back {
        width: 1920px;
        height: 1080px;
        background-color: rgba(0, 0, 0, 0.5);
        position: absolute;
        top: -8px;
        left: 8px;
    }

    .info {
        position: absolute;
        top: 180px;
        left: 1353px;
        border-radius: 5px;
    }

    .MoreInfo {
        position: absolute;
        top: 485px;
        left: 1353px;
        border-radius: 5px;
    }
</style>