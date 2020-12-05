<template>
  <div class="data-box--container">
    <div class="data-box--icon-box">
      <a-icon :type="icon" style="font-size: 1.5rem;"></a-icon>
    </div>
    <div class="data-box--title">{{ title }}</div>
    <div class="data-box--value">{{ value }}</div>
  </div>
</template>

<script>
export default {
  name: 'DataBox',
  data() {
    return {

    }
  },
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
  }
}
</script>

<style lang="scss" scoped>
  .data-box--container {
    width: 11rem;
    background-color: #fff;
    box-shadow: 2px 2px 10px -3px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    transition: all .2s ease;
    text-align: center;
    
    &:hover {
      cursor: pointer;
      color: $theme-color;
      transition: all .2s ease;
    }

    .data-box--icon-box {
      height: 3rem;
      width: auto;
      position: relative;

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

    .data-box--title {
      margin-top: .5rem;
      font-size: .9rem;
    }

    .data-box--value {
      font-size: 2rem;
      font-weight: bold;
      height: 2.5rem;
    }
  }
</style>