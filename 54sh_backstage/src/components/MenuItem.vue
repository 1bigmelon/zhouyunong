<template>
  <div class="menu-item--container">
    <div class="menu-item--content-container">
      <div class="menu-item--icon"></div>
      <a-icon type="form" />
      <span>新建文章</span>
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="scss" scoped>
//       background-color: rgb(242, 240, 254);
  .menu-item--container {
    height: 2.7rem;
    width: 100%;
    padding-left: calc(1.8rem - 3px);
    border-left: #FFF solid 3px;
    display: flex;
    align-items: center;
    color: rgb(123, 123, 126);

    &:hover {
      background-color: rgb(247, 247, 247);
      cursor: pointer;
      border-left: rgb(124, 97, 241) solid 3px;
      transition: border-left linear .2s;
    }

    .menu-item--content-container {
      span {
        margin-left: .8rem;
      }
    }
  }
</style>