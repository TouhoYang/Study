import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      // 监听/，使用redirect进行重定向
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      // 注意这里，有一个是components，是会报错的。
      component: Login
    },
    {
      path: '/home',
      component: Home
    }
  ]
})
// 挂在路由导航守卫
router.beforeEach((to, from, next) => {
  // to 将要访问的路径
  // from 代表 从哪个路径跳转而来
  // next 是一个函数，白哦是放行
  //    next（）放行     next（'/login'） 强制跳转
  if (to.path === '/login') return next()
  // 获取token
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()
})

export default router
