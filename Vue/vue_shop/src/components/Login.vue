<template>
  <div class="login_container">
    登录组件
  </div>
</template>

<script>
export default {}
</script>

<!--
lang = "less" 这个节点中支持less语法
scoped 是一个vue的指令，用来控制组件的样式的生效的区间；加上scoped，只在当前组件的样式生效
-->
<style lang="less" scoped>//注意：这里老师要求使用vue ui安装less—loader，但是我们现在安装的版本太高了会导致报错，所以我们卸载了，或者不装然后在下面终端输入npm install less-loader@5.0.0安装好了就可以了，后面的less可以正常在vue ui里面安装
.login_container{
  background-color: #2b4b6b;
  height: 100%;
}
</style>
