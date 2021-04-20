// 入口文件
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
// 导入全局样式表
import './assets/css/global.css'
// 导入字体图标
import './assets/fonts/iconfont.css'

// 配置axios
import axios from 'axios'
// 配置请求的路径,全局设置没有生效
// axios.default.baseURL = 'http://127.0.0.1:8888/api/private/v1/'、
// 使用实例化进行
const instance = axios.create({
  baseURL: 'http://127.0.0.1:8888/api/private/v1/'
})
axios.interceptors.request.use(config => {
  console.log(config)
  return config
})
Vue.prototype.$http = instance

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
