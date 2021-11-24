<template>
    <div id="app">
        <Home></Home>
    </div>
</template>
<!--????-->
<script>
    import Vue from 'vue'
    import ElementUI from 'element-ui';
    import 'element-ui/lib/theme-chalk/index.css';
    import router from './router/index'
    import Home from "./views/Home";

    //阻止vue在启动时生成生产提示
    Vue.config.productionTip = false
    Vue.use(ElementUI)

    export default {
        name: 'App',
        router,
        components: {
            Home,
        },
        beforeCreate() {
            Vue.prototype.$bus = this  //安装全局事件总线,$bus就是当前应用的vm
        },
    }
</script>

<style>
</style>
