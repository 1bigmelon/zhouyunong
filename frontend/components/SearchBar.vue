<template>
  <section class = "head">
      <div class="HeadContain">
        <a href = "#"><img class = "logo" src = "http://54sh.csu.edu.cn/static/img/logo2.png"></a>
        <div class="HeadRight">
          <div class = "HeadButton">
            <a class = "HeadHref" href = "#">首页</a>
          </div>
          <div class = "HeadButton">
            <a class = "HeadHref" href = "#">团委概况</a>
          </div>
          <div class = "HeadButton">
            <a class = "HeadHref" href = "#">网站文稿</a>
          </div>
          <div class = "HeadButton">
            <a class = "HeadHref" href = "#">投稿</a>
          </div>
          <div class = "HeadButton">
            <a class = "HeadHref" href = "#">指南</a>
          </div>
          <div class = "HeadButton">
            <a class = "HeadHref" href = "#">精品名栏</a>
          </div>
          <div class="SearchBar">
          </div>
        </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SearchBar',
}
</script>

<style scoped>
.head {
  width: 100vw;
  height:50px;
  background-color: red;
  opacity: 0.6;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.HeadContain{
  margin: 0 auto;
  padding: 0 auto;
  height:100%;
  width:1200px;
  max-width:1200vw;
  min-width: 960px;
  border:0px solid black;
  text-align: left;
}
.logo{
  height: 90%;
}
.HeadRight{
  display:flex;
  float:right;
  height: 100%;
  width: 800px;
  justify-content: space-around;
}
.HeadButton{
  text-align: center;
  height:95%;
  padding:10px 0;
  width:80px;
}
.HeadHref{
    color:white;
    text-decoration: none;
}
</style>
