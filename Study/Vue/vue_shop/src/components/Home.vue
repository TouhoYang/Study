<template>
    <!-- home 组件 -->
<!--    <div>
      <el-button type="info" @click="logout">退出</el-button>
    </div> -->
  <el-container class="home-container">
    <!-- 头部区 -->
    <el-header>
      <div>
        <img src="../assets/heima.png" alt="">
        <span>电商后台管理系统</span>
      </div>
      <el-button type="info" @click="logout">退出</el-button>
    </el-header>
      <!-- 页面主体区 -->
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="200px">
        <!-- 侧边栏菜单区 -->
        <!-- 这里如果正常编写会显示四个报错,原因是下面的open，close两个没有方法调用 -->
              <!-- @open="handleOpen"
              @close="handleClose" -->
        <el-menu
              default-active="2"
              class="el-menu-vertical-demo"
              background-color="#333744"
              text-color="#fff"
              active-text-color="#ffd04b">
              <!-- 一级菜单 -->
              <el-submenu index="1">
                <!-- 一级菜单的模板区 -->
                <template slot="title">
                  <!-- i 是图标 -->
                  <i class="el-icon-location"></i>
                  <!-- 文本 -->
                  <span>导航一</span>
                </template>
                <!-- 二级菜单 -->
                <el-menu-item index="1-1">
                  <template slot="title">
                    <i class="el-icon-location"></i>
                    <span>选项一</span>
                  </template>
                </el-menu-item>
              </el-submenu>
            </el-menu>
      </el-aside>
      <!-- 右侧内容主体 -->
      <el-main>Main</el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  methods: {
    logout () {
      // 清空token
      window.sessionStorage.clear()
      // 重定向到登录页面
      this.$router.push('/login')
    }
  }
}
</script>

<style>
  .home-container{
    height: 100%;
  }

.el-header{
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  /* el-header 拥有默认的填充 */
  padding-left: 0;
  align-items: center;
  color: #fff;
  font-size: 20px;
}

.el-header>div {
  display: flex;
  align-items: center;
}

span {
    margin-left: 15px;
}

.el-aside{
  background-color: #333744;
}

.el-main{
  background-color: #EAEDF1;
}
</style>
