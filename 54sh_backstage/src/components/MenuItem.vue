<template>
  <div :class="isSelected ? 'selected' : 'unselected'" @click="onClick">
    <div class="menu-item--container">
      <div class="menu-item--content-container">
        <a-icon :type="icon" />
        <span>{{ text }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'MenuItem',
  props: {
    text: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: 'windows'
    },
    name: {
      type: String,
      default: 'MenuItem'
    },
    to: {
      type: String,
      default: '/index'
    }
  },
  data() {
    return {
      isSelected: false
    }
  },
  computed: {
    ...mapState(['selectedItemName'])
  },
  watch: {
    selectedItemName(newVal) {
      this.isSelected = (newVal === this.name)
    }
  },
  mounted() {
    this.isSelected = (this.name === this.selectedItemName)
  },
  methods: {
    ...mapActions(['setSelectedItemName']),

    onClick() {
      if (this.name === 'logout') {
        this.$emit('click')
        return
      }
      this.setSelectedItemName(this.name)
      this.$router.push(this.to)
    }
  }
}
</script>

<style lang="scss" scoped>
  .menu-item--container {
    height: 2.9rem;
    width: 100%;
    border-left: #FFF solid 3px;
    display: flex;
    align-items: center;
    color: rgb(123, 123, 126);
    cursor: pointer;

    .menu-item--content-container {
      span {
        margin-left: .8rem;
      }
    }
  }

  .selected {
    background-color: rgb(242, 240, 254);
    border-left: $theme-color solid 3px;
    box-shadow: 0 0 1px 1px rgb(240, 238, 248) inset;

    .menu-item--container {
      padding-left: 1.8rem;
      color: $theme-color;
      transition: background-color linear .15s;
      border: none;
    }
  }

  .unselected {
    transition: background-color linear .15s;

    .menu-item--container {
      padding-left: 1.8rem;
      transition: background-color linear .15s;
    }

    &:hover .menu-item--container {
      background-color: rgb(247, 247, 247);
      border-left: $theme-color solid 3px;
      transition: all linear .15s;
    }
  }
</style>
