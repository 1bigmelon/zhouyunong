<template>
  <div class="container">
    <div class="data-box">
      <data-box icon="team" title="分类总数" :value="totalCategory" @click="dataBoxHdl"/>
      <data-box icon="user" title="启用中分类数" :value="enabledCategory" @click="dataBoxHdl({ status: '使用中' })"/>
      <data-box icon="user-delete" title="已停用分类数" :value="disabledCategory" @click="dataBoxHdl({ status: '已停用' })"/>
    </div>
    <div class="content-box">
      <div class="search-box">
        <a-form class="form" :form="form" label-align="right" layout="inline" @submit="search">
          <a-form-item label="分类名称">
            <a-input v-decorator="rules['categoryName']" placeholder="分类名称" />
          </a-form-item>
          <a-form-item label="所属组织">
            <a-select v-decorator="rules['role']" placeholder="分类所属组织" style="width: 10rem;">
              <a-select-option v-for="(item, index) in orgList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="分类状态">
            <a-select v-decorator="rules['status']" placeholder="分类状态" style="width: 10rem;">
              <a-select-option key="all" value="all">全部</a-select-option>
              <a-select-option key="enabled" value="使用中">使用中</a-select-option>
              <a-select-option key="disabled" value="已停用">已停用</a-select-option>
            </a-select>
          </a-form-item>
          <div class="operation-box">
            <a-button ref="submit" type="primary" html-type="submit" :loading="searching">搜索</a-button>
            <a-popconfirm title="确定清空？" ok-text="确定" cancel-text="取消" @confirm="reset">
              <a style="font-size: .9rem; margin-left: 1rem;">清空</a>
            </a-popconfirm>
          </div>
        </a-form>
      </div>
      <a-spin tip="加载中..." :delay="100" size="large" :spinning="loading">
        <a-icon slot="indicator" type="loading" spin />
        <div class="list-box">
          <a-table :columns="columns" row-key="id" :data-source="categoryList" :pagination="false">
            <template slot="description" slot-scope="text">
              <span>{{ text ? text : '无' }}</span>
            </template>
            <template slot="status" slot-scope="text, record">
              <span :style="`color: ${record.status ? '#0de20d' : '#fc243a'};`">{{ text }}</span>
            </template>
            <template slot="operation" slot-scope="text, record">
              <a-button
                type="primary"
                size="small"
                style="font-size: .7rem; margin-right: .5rem;"
                @click="edit(record.id)"
              >编辑</a-button>
              <a-button
                :type="record.status ? 'danger' : 'default'"
                :class="record.status ? '' : 'button-color-green'"
                size="small"
                style="font-size: .7rem;"
                @click="record.status ? disable(record.id) : enable(record.id)"
              >{{ record.status ? '停用' : '启用' }}</a-button>
            </template>
          </a-table>
          <a-pagination
            :current="nowPage"
            show-quick-jumper
            :total="totalCategory"
            class="pagination"
            @change="pageChange"
          ></a-pagination>
        </div>
      </a-spin>
    </div>
  </div>
</template>

<script>


import DataBox from '@/components/DataBox'
import moment from 'moment'

const columns = [
  {
    title: '分类名称',
    key: 'categoryName',
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
    title: '分类状态',
    key: 'status',
    dataIndex: 'statusText',
    width: '5%',
    align: 'center',
    scopedSlots: { customRender: 'status' }
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
  inject: ['refresh'],
  name: 'ManageCategory',
  components: {
    DataBox
  },
  data() {
    return {
      totalCategory: -1,
      enabledCategory: -1,
      disabledCategory: -1,
      form: this.$form.createForm(this, { name: 'category_search' }),
      rules: {
        headquarters: ['headquarters'],
        categoryName: ['categoryName'],
        role: ['role', {
          initialValue: 'all'
        }],
        status: ['status', {
          initialValue: 'all'
        }]
      },
      orgList: [],
      searching: false,
      columns,
      categoryList: [],
      loading: true,
      nowPage: 1

    }
  },
  mounted() {
    Promise.all([
      this.$api.getCategoriesByPageNum(1),
      this.$api.getAllOrgs(),
      this.$api.getAllCategories(),
    ]).then((res) => {
      res.forEach((item) => {
        if (!item.data.status) {
          return Promise.reject(new Error(item.data.msg))
        }
      })
      // console.log(res[0].data.data)
      const { divs } = res[0].data.data
      console.log(res[0].data.data)
      console.log(divs)
      this.categoryList = divs.map((item) => Object.assign(item, {
        // eslint-disable-next-line camelcase
        last_modify: moment.parseZone(item.last_modify.substr(5, item.last_modify.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
        statusText: item.status ? '使用中' : '已停用'
      }))
      this.totalCategory = divs.length

      this.orgList = [
        {
          name: '全部',
          id: 'all'
        },
        ...res[1].data.data.orgs
      ]
      this.loading = false
    }).catch((err) => {
      this.$message.error(err.message)
    })
  },
  methods: {
    reset() {
      this.form.setFieldsValue({
        headquarters: '',
        categoryName: '',
        organization: 'all',
        status: 'all'
      })
      this.$refs.submit.$el.click()
      this.$message.success('搜索条件已清空')
    },

    search(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (err) {
          this.$message.error('请检查是否填写正确')
          return
        }

        const criteria = {}
        for (const key in JSON.parse(JSON.stringify(values))) {
          if (['all', ''].includes(values[key])) continue

          if (key === 'status') {
            values[key] = (values[key] === '使用中')
          }
          Object.defineProperty(criteria, key, {
            value: values[key],
            enumerable: true
          })
        }

        this.searching = this.loading = true
        this.$api.searchCategory(criteria)
          .then((res) => {
            if (!res.data.status) {
              return Promise.reject(new Error(res.data.msg))
            }
            // console.log(res.data.data.divs)
            this.categoryList = res.data.data.divs.map((item) => Object.assign(item, {
              // eslint-disable-next-line camelcase
              last_modify: moment.parseZone(item.last_modify.substr(5, item.last_modify.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
              statusText: item.status ? '使用中' : '已停用'
            }))
          })
          .catch((err) => {
            this.$message.error(err?.message)
          })
          .finally(() => {
            this.searching = this.loading = false
          })
      })

    },

    edit(id) {
      this.$router.push(`/category/edit/${id}`)
    },

    disable(id) {
      const that = this

      this.$modal.confirm({
        title: '确认停用',
        content: '确定要停用该标签吗？停用后带有该标签的文章也会不可访问！',
        okText: '确定',
        cancelText: '取消',
        onOk() {
          that.$api.disableCategory(id)
            .then((res) => {
              if (!res.data.status) {
                return Promise.reject(new Error(res.data.msg))
              }
              that.$message.success('成功停用该分类')
              that.refresh()
            })
            .catch((err) => {
              this.$message.error(err.message)
            })
        }
      })
    },

    enable(id) {
      const that = this

      this.$modal.confirm({
        title: '确认启用',
        content: '确定要启用该分类吗？',
        okText: '确定',
        cancelText: '取消',
        onOk() {
          that.$api.enableCategory(id)
            .then((res) => {
              if (!res.data.status) {
                return Promise.reject(new Error(res.data.msg))
              }
              that.$message.success('成功启用该分类')
              that.refresh()
            })
            .catch((err) => {
              this.$message.error(err.message)
            })
        }
      })
    },
    pageChange(page) {
      this.nowPage = page
      this.loading = true
      this.$api.getCategoriesByPageNum(page)
        .then((res) => {
          if (!res.data.status) {
            return Promise.reject(new Error(res.data.msg))
          }

          this.categoryList = res.data.data.divs
        })
        .catch((err) => {
          this.$message.error(err.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    dataBoxHdl(preset = {}) {
      this.form.setFieldsValue(Object.assign({
        headquarters: '',
        categoryName: '',
        organization: 'all',
        status: 'all'
      }, preset))
      this.$refs.submit.$el.click()
    }
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

    .pagination {
        text-align: right;
        margin: {
          top: 1.5rem;
          bottom: .5rem;
          right: 1.5rem;
        }
      }
  }
}
</style>
