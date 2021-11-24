import VueRouter from "vue-router";
import Login from "../views/Login";
import Reg from "../views/Reg";
import Home from "../views/Home";
import App from "../App";
import Info from '../components/Info'
import InfoInit from '../components/InfoInit'
import Title from "../components/Title";
import InfoSet from "../components/InfoSet";
import Vue from "vue";
import Write from "../views/Write";
import Article from '../views/Article';
import CreateBar from "../views/CreateBar";
import Search from "../components/Search";
import Theme from "../views/Theme";
import BarSet from "../views/BarSet";

Vue.use(VueRouter)
//创建并暴露路由器
const router = new VueRouter({
    routes: [
        {
            name: 'barset',
            path: '/BarSet',
            component: BarSet
        },
        {
            name: 'theme',
            path: '/Theme',
            component: Theme
        },
        {
            name: 'search',
            path: '/Search',
            component: Search
        },
        {
            name: 'createBar',
            path: '/CreateBar',
            component: CreateBar
        },
        {
            name: 'article',
            path: '/Article',
            component: Article
        },
        {
            name: 'write',
            path: '/Write',
            component: Write
        },
        {
            name: 'info_set',
            path: '/InfoSet',
            component: InfoSet,
        },
        {
            name: 'login',
            path: '/login',
            component: Login
        }, {
            name: 'reg',
            path: '/reg',
            component: Reg
        },
        {
            name: 'home',
            path: '/home',
            component: Home,
            children: [ //通过children配置子级路由
                {
                    name: 'info',
                    path: 'Info',
                    component: Info
                }, {
                    name: 'info_init',
                    path: 'InfoInit',//子级路由一定不要写/InfoInit
                    component: InfoInit
                },
                {
                    name: 'title',
                    path: 'Title',
                    component: Title
                },
            ]

        },
        {
            name: 'app',
            path: '/App',
            component: App
        },

    ]
})

// router.beforeEach((to, from, next) => {
//     console.log('去>>>>', to, '从>>>>', from, '下一个>>>>', next)
//     console.log('username>>', Vue.store)
//     // if (to.query.article_id != 0) {
//     //
//     // }
//     next()
// })

export default router
// //解决重复点击导航功能
// const VueRouterPush = VueRouter.prototype.push
// VueRouter.prototype.push = function push(to) {
//     return VueRouterPush.call(this.to).catch(err => err)
// }
