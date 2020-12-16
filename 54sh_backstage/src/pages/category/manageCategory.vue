<template>
  <div class="container">
    <div class="data-box">
      <data-box icon="team" title="分类总数" :value="totalCategory" />
      <data-box icon="user" title="启用中分类数" :value="enabledCategory" />
      <data-box icon="user-delete" title="已停用分类数" :value="disabledCategory" />
    </div>
    <div class="content-box">
      <div class="search-box">
        还没想好搜索框怎么布局
      </div>
      <div class="list-box">
        <a-table :columns="columns" row-key="id">

        </a-table>
      </div>
    </div>
  </div>
</template>

<script>


import DataBox from '@/components/DataBox'

const columns = [
  {
    title: '分类总数',
    key: 'headquarters',
    dataIndex: '',
    width: '10%',
    align: 'center'
  },
  {
    title: '分类名称',
    key: 'categroyName',
    dataIndex: 'name',
    width: '',
    align: 'center'
  },
  {
    title: '所属组织',
    key: 'role',
    dataIndex: '',
    width: '',
    align: 'center'
  },
  {
    title: '分类描述',
    key: 'department',
    dataIndex: 'org.name',
    width: '',
    align: 'center'
  },
  {
    title: '分类最新更新时间',
    key: 'phone',
    dataIndex: 'phone',
    width: '',
    align: 'center'
  },
  {
    title: '更新内容使用id',
    key: 'email',
    dataIndex: 'email',
    width: '',
    align: 'center'
  },
  {
    title: '分类点击量',
    key: 'ip',
    dataIndex: 'last_ip',
    width: '',
    align: 'center'
  },
  {
    title: '是否发布',
    key: 'recentLoginTime',
    dataIndex: 'last_login',
    width: '',
    align: 'center'
  },
  {
    title: '操作',
    key: 'operation',
    width: '',
    align: 'center',
    scopedSlots: { customRender: 'operation' }
  }
]

export default {
  name: 'ManageCategory',
  components: {
    'data-box': DataBox
  },
  data() {
    return {
      totalCategory: -1,
      enabledCategory: -1,
      disabledCategory: -1,
      columns,
      categoryList: [],
    }
  },
  mounted() {
    this.$api.getAllCategories()
      .then((res) => {
        console.log(res)
        if (!res.data.status) {
          this.$message.error(res.data.msg)
          return Promise.resolve()
        }
        const { divs } = res.data.data
        this.categoryList = divs
        this.totalCategory = divs.length
        // this.enabledCategory = enable
        // this.disabledCategory = disable


      })
  },
  methods: {

  }
}
</script>

<style lang="scss" scoped>
.container {
  @extend .component;
  height: 100%;
    width: 100%;
    display: block;

    .data-box {
      @extend .data-box;
      width: 50rem;
      margin: 0 auto;
    }

    .content-box {
      @extend .component;
      margin-top: 1.5rem;
      width: 100%;

      .search-box {
        height: 7rem;
        width: 100%;
        background-color: pink;
      }
    }
}
</style>
