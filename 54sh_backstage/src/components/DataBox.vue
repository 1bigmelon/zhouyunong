<template>
  <div class="data-box--container">
    <div class="icon-box">
      <a-icon :type="icon" style="font-size: 1.5rem;"></a-icon>
    </div>
    <div class="title">{{ title }}</div>
    <div class="value">{{ value === -1 ? 'loading' : value }}</div>
  </div>
</template>

<script>
export default {
  name: 'DataBox',
  props: {
    icon: {
      type: String,
      default: 'home'
    },
    title: {
      type: String,
      default: ''
    },
    value: {
      type: Number,
      default: -1
    }
  },
  data() {
    return {

    }
  }
}
</script>

<style lang="scss" scoped>
  .data-box--container {
    @extend .component;

    width: 11rem;
    transition: color .2s ease;
    // transition: transform .4s ease;
    text-align: center;

    &:hover {
      cursor: pointer;
      color: $theme-color;
      // transform: translateY(-3px);
      transition: color .2s ease;
      // transition: transform .4s ease;
    }

    .icon-box {
      height: 3rem;
      width: auto;
      position: relative;
      z-index: 0;

      i {
        z-index: 999;
        position: absolute;
        left: calc(50% - 0.75rem);
        top: calc(50% - 0.75rem);

        &:after {
          content: "";
          position: absolute;
          left: calc(50% - 1.5rem);
          top: calc(50% - 1.5rem);
          background-color: rgb(238, 238, 238);
          height: 3rem;
          width: 3rem;
          z-index: -1;
          border-radius: 50%;
        }
      }
    }

    .title {
      margin-top: .5rem;
      font-size: .9rem;
    }

    .value {
      font-size: 1.5rem;
      font-weight: bold;
      font-family: -apple-system, 'OpenSans', sans-serif;
    }
  }
</style>
