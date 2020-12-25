<template>
  <div class="container">
    <div class="data-box">
      <data-box icon="tags" title="标签总数" :value="totalTag" />
      <data-box icon="tag" title="启用中标签数" :value="enabledTag" />
      <data-box icon="minus-square" title="已停用标签数" :value="disabledTag" />
    </div>
    <div class="content-box">
      <!-- <div class="search-box">
        <a-form class="form" :form="form" label-align="right" layout="inline" @submit="search">
          <a-form-item></a-form-item>
        </a-form>
      </div> -->
      <div class="tag-list-box">
        <a-table :columns="columns" row-key="id" :data-source="showedList">

        </a-table>
      </div>
    </div>
  </div>
</template>

<script>
import DataBox from '@/components/DataBox'
import moment from 'moment'

const columns = [
  {
    title: '名称',
    key: 'name',
    dataIndex: 'name',
    width: '13%',
    align: 'center'
  },
  {
    title: '所属分类',
    key: 'category',
    dataIndex: '',
    width: '10%',
    align: 'center'
  },
  {
    title: '所属组织',
    key: 'organization',
    dataIndex: 'org.name',
    width: '12%',
    align: 'center'
  },
  {
    title: '描述',
    key: 'description',
    dataIndex: 'description',
    width: '18%'
  },
  {
    title: '最近修改时间',
    key: 'recentModifyTime',
    dataIndex: 'last_modify',
    width: '10%',
    align: 'center'
  },
  {
    title: '点击量',
    key: 'clicks',
    dataIndex: 'click',
    width: '8%',
    align: 'center'
  },
  {
    title: '状态',
    key: 'status',
    dataIndex: 'statusText',
    width: '5%',
    align: 'center'
  },
  {
    title: '操作',
    key: 'operation',
    width: '10%',
    align: 'center'
  },
]

export default {
  name: 'ManageTag',
  components: {
    DataBox
  },
  data() {
    return {
      totalTag: -1,
      enabledTag: -1,
      disabledTag: -1,
      form: this.$form.createForm(this, { name: 'tag_search' }),
      rules: {},
      categoryList: [],
      orgList: [],
      columns,
      tagList: [],
      showedList: []
    }
  },
  mounted() {
    Promise.all([
      this.$api.getAllTags(),
      this.$api.getAllOrgs(),
      this.$api.getAllCategories()
    ]).then((res) => {
      console.log('res: ', res)
      res.forEach((item) => {
        if (!item.data.status) {
          return Promise.reject(item.data.msg)
        }
      })

      const { tags } = res[0].data.data
      this.tagList = tags.map((item) => Object.assign(item, {
        // eslint-disable-next-line camelcase
        last_modify: moment.parseZone(item.last_modify.substr(5, item.last_modify.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
        statusText: item.status ? '使用中' : '已停用'
      }))
      this.showedList = this.tagList
      this.totalTag = tags.length

      this.orgList = res[1].data.data.orgs

      this.categoryList = res[2].data.data.divs
    })
  },
  methods: {

  }
}
</script>

<style lang="scss" scoped>
  .container {
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
        width: 100%;
        padding: .5rem 1rem;
        padding-bottom: 1.5rem;

        .form {
          height: 100%;
          width: 100%;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .operation-box {

          button {
            width: 5.5rem;
          }
        }
      }
    }
  }
</style>
