import Vue from 'vue'
import App from './App.vue'
import VueRouter from "vue-router";
//引入裁剪图片插件
import VueCropper from 'vue-cropper'
//引入store
import store from './store/index'
// 引入图标字体
import 'font-awesome/css/font-awesome.css'
//使用插件
Vue.use(VueRouter)
Vue.prototype.$server = 'http://127.0.0.1:8000/'
// 使用裁剪插件
Vue.use(VueCropper)


// 阻止vue 在启动时生成生产提示
Vue.config.productionTip = false

new Vue({
    store,
    render: h => h(App),
}).$mount('#app')
