<template>
  <div class="container">
    <div class="data-box">
      <data-box icon="tags" title="标签总数" :value="totalTag" @click="dataBoxHdl" />
      <data-box icon="tag" title="启用中标签数" :value="enabledTag" @click="dataBoxHdl({ status: '使用中' })" />
      <data-box icon="minus-square" title="已停用标签数" :value="disabledTag" @click="dataBoxHdl({ status: '已停用' })" />
    </div>
    <div class="content-box">
      <div class="search-box">
        <a-form class="form" :form="form" label-align="right" layout="inline" @submit="search">
          <a-form-item label="标签名称">
            <a-input v-decorator="rules['name']" placeholder="标签名称" />
          </a-form-item>
          <a-form-item label="所属分类">
            <a-select v-decorator="rules['category']" placeholder="标签所属分类" style="width: 10rem;">
              <a-select-option v-for="(item, index) in categoryList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="所属组织">
            <a-select v-decorator="rules['organization']" placeholder="标签所属组织" style="width: 10rem;">
              <a-select-option v-for="(item, index) in orgList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="标签状态">
            <a-select v-decorator="rules['status']" placeholder="标签状态" style="width: 10rem;">
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
        <div class="tag-list-box">
          <a-table :columns="columns" row-key="id" :data-source="tagList" :pagination="false">
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
            :total="totalTag"
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
    title: '名称',
    key: 'name',
    dataIndex: 'name',
    width: '',
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
    width: '22%',
    align: 'center',
    scopedSlots: { customRender: 'description' }
  },
  {
    title: '最近修改时间',
    key: 'recentModifyTime',
    dataIndex: 'last_modify',
    width: '13%',
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
    align: 'center',
    scopedSlots: { customRender: 'status' }
  },
  {
    title: '操作',
    key: 'operation',
    width: '10%',
    align: 'center',
    scopedSlots: { customRender: 'operation' }
  },
]

export default {
  inject: ['refresh'],
  name: 'ManageTag',
  components: {
    DataBox
  },
  data() {
    return {
      // data box
      totalTag: -1,
      enabledTag: -1,
      disabledTag: -1,
      // search
      form: this.$form.createForm(this, { name: 'tag_search' }),
      rules: {
        name: ['name'],
        category: ['category', {
          initialValue: 'all'
        }],
        organization: ['organization', {
          initialValue: 'all'
        }],
        status: ['status', {
          initialValue: 'all'
        }]
      },
      categoryList: [],
      orgList: [],
      searching: false,
      // table
      columns,
      tagList: [],
      loading: true,
      nowPage: 1
    }
  },
  mounted() {
    Promise.all([
      this.$api.getTagsByPageNum(1),
      this.$api.getAllOrgs(),
      this.$api.getAllCategories()
    ]).then((res) => {
      res.forEach((item) => {
        if (!item.data.status) {
          return Promise.reject(new Error(item.data.msg))
        }
      })

      const { tags } = res[0].data.data
      this.tagList = tags.map((item) => Object.assign(item, {
        // eslint-disable-next-line camelcase
        last_modify: moment.parseZone(item.last_modify.substr(5, item.last_modify.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
        statusText: item.status ? '使用中' : '已停用'
      }))
      this.totalTag = tags.length

      this.orgList = [
        {
          name: '全部',
          id: 'all'
        },
        ...res[1].data.data.orgs
      ]

      this.categoryList = [
        {
          name: '全部',
          id: 'all'
        },
        ...res[2].data.data.divs
      ]

      this.loading = false
    }).catch((err) => {
      this.$message.error(err.message)
    })
  },
  methods: {
    reset() {
      this.form.setFieldsValue({
        name: '',
        category: 'all',
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
        this.$api.searchTag(criteria)
          .then((res) => {
            if (!res.data.status) {
              return Promise.reject(new Error(res.data.msg))
            }
            this.tagList = res.data.data.tags.map((item) => Object.assign(item, {
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
      this.$router.push(`/tag/edit/${id}`)
    },
    disable(id) {
      const that = this

      this.$modal.confirm({
        title: '确认停用',
        content: '确定要停用该标签吗？停用后带有该标签的文章也会不可访问！',
        okText: '确定',
        cancelText: '取消',
        onOk() {
          that.$api.disableTag(id)
            .then((res) => {
              if (!res.data.status) {
                return Promise.reject(new Error(res.data.msg))
              }
              that.$message.success('成功停用该标签')
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
        content: '确定要启用该标签吗？',
        okText: '确定',
        cancelText: '取消',
        onOk() {
          that.$api.enableTag(id)
            .then((res) => {
              if (!res.data.status) {
                return Promise.reject(new Error(res.data.msg))
              }
              that.$message.success('成功启用该标签')
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
      this.$api.getTagsByPageNum(page)
        .then((res) => {
          if (!res.data.status) {
            return Promise.reject(new Error(res.data.msg))
          }

          this.tagList = res.data.data.tags
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
        name: '',
        category: 'all',
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
