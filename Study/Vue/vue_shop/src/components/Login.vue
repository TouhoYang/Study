<template>
  <div class="login_container">
    <!-- 登录组件 -->
    <div class= "login_box">
      <div class="avtar_box">
        <img src="../assets/logo.png" alt="">
      </div>
    </div>
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
.login_box{
  width: 450px;
  height: 300px;
  background-color: #fff;
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
    img{
      height: 100%;
      width: 100%;
      border-radius: 50%;
      background-color: #eee;
    }
  }
}
</style>
