<template>
  <div class="login_container">
    <!-- 登录组件 -->
    <div class= "login_box">
      <!-- 头像区 -->
      <div class="avtar_box">
        <img src="../assets/logo.png" alt="">
      </div>
      <!-- 表单区 -->
      <el-form ref='loginFormRef' :rules="loginFormRules" :model="loginForm" label-width="0px" class="login_form">
        <!-- 用户名 -->
        <el-form-item prop="username">
          <el-input
            prefix-icon="iconfont icon-user"
            v-model="loginForm.username">
          </el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input
            prefix-icon="iconfont icon-3702mima"
            v-model="loginForm.password"
            type="password">
          </el-input>
        </el-form-item>
        <!-- 按钮 -->
        <el-form-item class="btns">
          <el-button type="primary" round @click="login">登录</el-button>
          <el-button type="info" round @click="resetLoginForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 这是登录表单的数据绑定对象
      loginForm: {
        username: 'admin',
        password: '123456'
      },
      // 表单验证规则对象
      loginFormRules: {
        // 验证用户名是否合法
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 5, max: 10, message: '长度在 5 到 10 个字符', trigger: 'blur' }
        ],
        // 验证密码是否合法
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 5, max: 15, message: '长度在 5 到 15 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 点击重置按钮，点击重置表单
    resetLoginForm () {
      // 可以使用多个方法，不需要添加分号即可
      console.log(this)
      // 这里不用添加分号
      this.$refs.loginFormRef.resetFields()
    },
    login () {
      this.$refs.loginFormRef.validate(async (valid) => {
        // 视频22P
        // console.log(valid)
        // if (!valid) return
        // 视频上的使用login由于不明原因导致了请求时的地址变成了192.168.1.106：8080的地址 没有正常连接上接口，所以这里直接使用完整的地址进行链接
        const { data: res } = await this.$http.post('login', this.loginForm)
        // console.log(res)
        if (res.meta.status !== 200) return this.$message.error('登录失败')
        this.$message.success('登录成功')
        // 1.将登录成功之后的token保存到客户端的sessionStorage中
        //   1.1项目中除了登录之外的其他API接口必须在用户登录了之后才能访问
        //   1.2token只能在当前网站打开期间生效,所以将token保存在sessionStorage中
        console.log(res)
        window.sessionStorage.setItem('token', res.data.token)
        // 2.通过编程式导航跳转到后台主页,路由地址为"/home"
        this.$router.push('/home')
      })
    }
  }
}
</script>

<!--
lang = "less" 这个节点中支持less语法
scoped 是一个vue的指令，用来控制组件的样式的生效的区间；加上scoped，只在当前组件的样式生效
-->
<style lang="less" scoped>//注意：这里老师要求使用vue ui安装less—loader，但是我们现在安装的版本太高了会导致报错，所以我们卸载了，或者不装然后在下面终端输入npm install less-loader@5.0.0安装好了就可以了，后面的less可以正常在vue ui里面安装
.login_container{
  background-color:#2b4b6b;
  height: 100%;
}
.login_box{
  width: 450px;
  height: 300px;
  background-color:#fff;
  // 圆角属性
  border-radius: 3px;
  // 绝对定位
  position: absolute;
  left: 50%;
  top: 50%;
  // 当使用：top: 50%;left: 50%;， 是以左上角为原点，故不处于中心位置
  // translate(-50%,-50%) 作用是，往上（x轴）,左（y轴）移动自身长宽的 50%，以使其居于中心位置
  transform: translate(-50%,-50%);
  .avtar_box{
    height: 130px;
    width: 130px;
    // 正方形的边框
    border: 1px solid #eee;
    border-radius: 50%;
    //给图片和边框加一个10px边距
    padding: 10px;
    box-shadow: 0 0 10px #ddd;
    position: absolute;
    left: 50%;
    transform: translate(-50%,-50%);
    transform: tans;
    background-color: #fff;
    img{
      height: 100%;
      width: 100%;
      border-radius: 50%;
      background-color: #eee;
    }
  }
}

.login_form{
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0px 20px;
  box-sizing: border-box;
}

.btns{
  // display: flex设置为弹性布局，
  // justify-content: flex-end项目位于容器的结尾。
  display: flex;
  justify-content: flex-end;
}

</style>
