<template>
  <div class="container">
    <div class="data-box">
      <data-box icon="team" title="用户总数" :value="totalUser" />
      <data-box icon="user" title="启用中用户数" :value="enabledUser" />
      <data-box icon="user-delete" title="已停用用户数" :value="disabledUser" />
    </div>
    <div class="content-box">
      <div class="search-box">
        还没想好搜索框怎么布局
      </div>
      <div class="user-list-box">
        <a-table :columns="columns" row-key="id" :data-source="userList">
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
            >停用</a-button>
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
    key: 'realname',
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
    align: 'center'
  },
  {
    title: '最近登录IP',
    key: 'ip',
    dataIndex: 'last_ip',
    width: '10%',
    align: 'center'
  },
  {
    title: '最近登录时间',
    key: 'recentLoginTime',
    dataIndex: 'last_login',
    width: '',
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
      columns,
      userList: []
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
        this.userList = users.map((item) => {
          return Object.assign(item, {
            // eslint-disable-next-line camelcase
            last_login: moment.parseZone(item.last_login.substr(5, item.last_login.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'),
            statusText: item.status ? '使用中' : '已停用'
          })
        })
        this.totalUser = users.length
        this.enabledUser = enabled
        this.disabledUser = disabled
      })
  },
  methods: {
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
              console.log(res)
              if (res.data.status) {
                that.$message.success('成功停用该用户')
                that.refresh()
                return Promise.resolve()
              }
              else {
                return Promise.reject()
              }
            })
        },
        onCancel() {}
      })
    },
    enable(id) {
      console.log('enable', id)

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
        height: 7rem;
        width: 100%;
        background-color: pink;
      }
    }
  }
</style>
