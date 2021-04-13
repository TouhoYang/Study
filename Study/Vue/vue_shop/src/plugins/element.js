import Vue from 'vue'
// 按照老师的写法这里会报错，imported multiple times  import/no-duplicates
// 大致意思是重复地导入了信息，所以我们把这些数据整合起来成一条导入信息就可以了。
import { Button, Form, FormItem, Input } from 'element-ui'

Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
