<template>
  <div class="container">
    <div class="data-box">
      <data-box icon="team" title="用户总数" :value="totalUser" />
      <data-box icon="user" title="启用中用户数" :value="enabledUser" />
      <data-box icon="user-delete" title="已停用用户数" :value="disabledUser" />
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
              <a-select-option key="enabled" :value="1">使用中</a-select-option>
              <a-select-option key="disabled" :value="0">已停用</a-select-option>
            </a-select>
          </a-form-item>
          <div class="operation-box">
            <a-button type="primary" html-type="submit" :loading="searching">搜索</a-button>
            <a-popconfirm title="确定清空？" ok-text="确定" cancel-text="取消" @confirm="reset">
              <a style="font-size: .9rem; margin-left: 1rem;">清空</a>
            </a-popconfirm>
          </div>
        </a-form>
      </div>
      <div class="user-list-box">
        <a-table :columns="columns" row-key="id" :data-source="showedList">
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
      </div>
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
      totalUser: -1,
      enabledUser: -1,
      disabledUser: -1,
      form: this.$form.createForm(this, { name: 'search' }),
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
      columns,
      userList: [],
      showedList: []
    }
  },
  mounted() {
    this.$api.getAllUsers()
      .then((res) => {
        if (!res.data.status) {
          this.$message.error(res.data.msg)
          return Promise.resolve()
        }
        const { users, enabled, disabled } = res.data.data
        this.userList = users.map((item) => Object.assign(item, {
          // eslint-disable-next-line camelcase
          last_login: moment.parseZone(item.last_login.substr(5, item.last_login.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
          statusText: item.status ? '使用中' : '已停用',
          department: item.org?.id
        }))
        this.showedList = this.userList
        this.totalUser = users.length
        this.enabledUser = enabled
        this.disabledUser = disabled
      })

    this.$api.getAllOrgs()
      .then((res) => {
        if (!res.data.status) {
          return Promise.reject(res.data.msg)
        }
        this.orgList = [
          {
            name: '全部',
            id: 'all'
          },
          ...res.data.data.orgs
        ]
      })
      .catch((err) => {
        this.$message.error(err?.message)
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
      this.showedList = this.userList
      this.$message.success('搜索条件已清空')
    },
    search(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (err) {
          this.$message.error(err)
          return
        }

        const criteria = {}
        for (const key in JSON.parse(JSON.stringify(values))) {
          if (values[key] === 'all') continue

          if (key === 'status') {
            values[key] = (values[key] === 1)
          }
          Object.defineProperty(criteria, key, {
            value: values[key],
            enumerable: true
          })
        }
        console.log('criteria: ', criteria)

        this.showedList = this.userList.filter((item) => {
          let flag = true
          for (const key in criteria) {
            console.log('item[key]: ', item[key])
            console.log('criteria[key]: ', criteria[key])
            if (item[key] !== criteria[key]) {
              flag = false
              break
            }
          }
          console.log('flag: ', flag)
          return flag
        })
        this.$message.success('搜索成功')

        // this.searching = true
        // this.$api.searchUsers(criteria)
        //   .then((res) => {
        //     console.log(res.data)
        //     if (!res.data.status) {
        //       return Promise.reject(res.data.msg)
        //     }
        //     this.userList = res.data.data.users.map((item) => Object.assign(item, {
        //       // eslint-disable-next-line camelcase
        //       last_login: moment.parseZone(item.last_login.substr(5, item.last_login.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
        //       statusText: item.status ? '使用中' : '已停用'
        //     }))
        //     this.$message.success('搜索成功')
        //   })
        //   .catch((err) => {
        //     this.$message.error(err?.message)
        //   })
        //   .finally(() => {
        //     this.searching = false
        //     this.reset()
        //   })
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
          that.$api.disableUser({ id })
            .then((res) => {
              console.log(res.data)
              if (!res.data.status) {
                return Promise.reject(res.data.msg)
              }
              that.$message.success('成功停用该用户')
              that.refresh()
            })
            .catch((err) => {
              this.$message.error(err?.message)
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
          that.$api.changeUserInfo({ id, status: true })
            .then((res) => {
              console.log(res.data)
              if (!res.data.status) {
                return Promise.reject(res.data.msg)
              }
              that.$message.success('成功启用该用户')
              that.refresh()
            })
            .catch((err) => {
              this.$message.error(err?.message)
            })
        },
        onCancel() {}
      })
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
    }
  }
</style>
