import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'

Vue.use(VueRouter)

const routes = [
  {
    // 监听/，使用redirect进行重定向
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    // 注意这里，有一个是components，是会报错的。
    component: Login
  }
]

const router = new VueRouter({
  routes
})

export default router
