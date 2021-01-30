<template>
  <div class = "main">
    <section class="head">
      <SearchBar></SearchBar>
    </section>
    <nuxt/>
    <section class = "tail"></section>
  </div>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'

export default {
  components: {
    SearchBar,
  },
}
</script>
<style>
html {
  font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
  background-color: #fff;
}

*, *:before, *:after {
  box-sizing: border-box;
  margin: 0;
}

.button--green {
  display: inline-block;
  border-radius: 4px;
  border: 1px solid #3b8070;
  color: #3b8070;
  text-decoration: none;
  padding: 10px 30px;
}

.button--green:hover {
  color: #fff;
  background-color: #3b8070;
}

.button--grey {
  display: inline-block;
  border-radius: 4px;
  border: 1px solid #35495e;
  color: #35495e;
  text-decoration: none;
  padding: 10px 30px;
  margin-left: 15px;
}

.button--grey:hover {
  color: #fff;
  background-color: #35495e;
}
.tail{
  bottom:0px;
  min-width: 100vh;
  height:200px;
  background-color: #f6f9fa;
  opacity: 0.6;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>
