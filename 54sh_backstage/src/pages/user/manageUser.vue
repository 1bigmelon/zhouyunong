<template>
  <div class="container">
    <div class="data-box">
      <data-box icon="team" title="用户总数" :value="totalUser" @click="dataBoxHdl" />
      <data-box icon="user" title="启用中用户数" :value="enabledUser" @click="dataBoxHdl({ status: '使用中' })" />
      <data-box icon="user-delete" title="已停用用户数" :value="disabledUser" @click="dataBoxHdl({ status: '已停用' })" />
    </div>
    <div class="content-box">
      <div class="search-box">
        <a-form class="form" :form="form" label-align="right" layout="inline" @submit="search">
          <a-form-item label="真实姓名">
            <a-input v-decorator="rules['name']" placeholder="用户真实姓名" />
          </a-form-item>
          <a-form-item label="权限角色">
            <a-select v-decorator="rules['role']" placeholder="用户权限角色" style="width: 10rem;">
              <a-select-option key="all" value="all">全部</a-select-option>
              <a-select-option key="FirstAudit" value="一审">一审</a-select-option>
              <a-select-option key="SecondAudit" value="二审">二审</a-select-option>
              <a-select-option key="FinalAudit" value="终审">终审</a-select-option>
              <a-select-option key="Admin" value="管理员">管理员</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="所属部门">
            <a-select v-decorator="rules['department']" placeholder="用户所属部门" style="width: 10rem;">
              <a-select-option v-for="(item, index) in orgList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="用户状态">
            <a-select v-decorator="rules['status']" placeholder="用户状态" style="width: 10rem;">
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
        <div class="low-height-list-box">
          <a-table :columns="columns" row-key="id" :data-source="userList" :pagination="false">
            <template slot="email" slot-scope="text">
              <span>{{ text ? text : '-' }}</span>
            </template>
            <template slot="ip" slot-scope="text">
              <span>{{ text ? text : '-' }}</span>
            </template>
            <template slot="recentLoginTime" slot-scope="text">
              <span>{{ text ? text : '-' }}</span>
            </template>
            <template slot="status" slot-scope="text, record">
              <span :style="`color: ${record.status ? '#0de20d' : '#fc243a'};`">{{ text }}</span>
            </template>
            <template slot="operation" slot-scope="text, record">
              <a-button
                type="primary"
                size="small"
                style="font-size: .7rem; margin-right: .5rem;"
                @click="edit(record.user_id)"
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
            :total="totalUser"
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
    title: '用户名',
    key: 'username',
    dataIndex: 'user_id',
    width: '8%',
    align: 'center'
  },
  {
    title: '真实姓名',
    key: 'name',
    dataIndex: 'name',
    width: '8%',
    align: 'center'
  },
  {
    title: '权限角色',
    key: 'role',
    dataIndex: 'role',
    width: '10%',
    align: 'center'
  },
  {
    title: '所属部门',
    key: 'department',
    dataIndex: 'org.name',
    width: '10%',
    align: 'center'
  },
  {
    title: '手机号码',
    key: 'phone',
    dataIndex: 'phone',
    width: '10%',
    align: 'center'
  },
  {
    title: '邮箱',
    key: 'email',
    dataIndex: 'email',
    width: '15%',
    align: 'center',
    scopedSlots: { customRender: 'email' }
  },
  {
    title: '最近登录IP',
    key: 'ip',
    dataIndex: 'last_ip',
    width: '10%',
    align: 'center',
    scopedSlots: { customRender: 'ip' }
  },
  {
    title: '最近登录时间',
    key: 'recentLoginTime',
    dataIndex: 'last_login',
    width: '',
    align: 'center',
    scopedSlots: { customRender: 'recentLoginTime' }
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
  }
]

export default {
  inject: ['refresh'],
  name: 'ManageUser',
  components: {
    'data-box': DataBox
  },
  data() {
    return {
      loading: true,
      // search
      form: this.$form.createForm(this, { name: 'user_search' }),
      rules: {
        name: ['name'],
        role: ['role', {
          initialValue: 'all'
        }],
        department: ['department', {
          initialValue: 'all'
        }],
        status: ['status', {
          initialValue: 'all'
        }]
      },
      orgList: [],
      searching: false,
      // table
      columns,
      userList: [],
      // pagination
      nowPage: 1,
      // data box
      totalUser: -1,
      enabledUser: -1,
      disabledUser: -1,
    }
  },
  mounted() {
    Promise.all([this.$api.getUsersByPageNum(1), this.$api.getAllOrgs()])
      .then((res) => {
        res.forEach((item) => {
          if (!item.data.status) {
            return Promise.reject(new Error(item.data.msg))
          }
        })

        const { users, enabled, disabled, tot, pages } = res[0].data.data
        this.userList = users.map((item) => Object.assign(item, {
          // eslint-disable-next-line camelcase
          last_login: moment.parseZone(item.last_login.substr(5, item.last_login.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
          statusText: item.status ? '使用中' : '已停用',
          department: item.org?.id
        }))
        this.totalUser = tot
        this.enabledUser = enabled
        this.disabledUser = disabled

        this.orgList = [
          {
            name: '全部',
            id: 'all'
          },
          ...res[1].data.data.orgs
        ]

        this.loading = false
      })
      .catch((err) => {
        this.$message.error(err.message)
      })
  },
  methods: {
    reset() {
      this.form.setFieldsValue({
        name: '',
        role: 'all',
        department: 'all',
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
        this.$api.searchUsers(criteria)
          .then((res) => {
            if (!res.data.status) {
              return Promise.reject(new Error(res.data.msg))
            }
            this.userList = res.data.data.users.map((item) => Object.assign(item, {
              // eslint-disable-next-line camelcase
              last_login: moment.parseZone(item.last_login.substr(5, item.last_login.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
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
    edit(username) {
      this.$router.push(`/user/edit/${username}`)
    },
    disable(id) {
      const that = this

      this.$modal.confirm({
        title: '确认停用',
        content: '确定要停用该用户吗？',
        okText: '确定',
        cancelText: '取消',
        onOk() {
          that.$api.disableUser(id)
            .then((res) => {
              if (!res.data.status) {
                return Promise.reject(new Error(res.data.msg))
              }
              that.$message.success('成功停用该用户')
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
        content: '确定要启用该用户吗？',
        okText: '确定',
        cancelText: '取消',
        onOk() {
          that.$api.enableUser(id)
            .then((res) => {
              if (!res.data.status) {
                return Promise.reject(new Error(res.data.msg))
              }
              that.$message.success('成功启用该用户')
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
      this.$api.getUsersByPageNum(page)
        .then((res) => {
          if (!res.data.status) {
            return Promise.reject(new Error(res.data.msg))
          }

          this.userList = res.data.data.users
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
        role: 'all',
        department: 'all',
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
