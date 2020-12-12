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
      <div class="list-box">
        <a-table :columns="columns" row-key="id">

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
    width: '10%',
    align: 'center'
  },
  {
    title: '真实姓名',
    key: 'realname',
    dataIndex: 'name',
    width: '',
    align: 'center'
  },
  {
    title: '权限角色',
    key: 'role',
    dataIndex: '',
    width: '',
    align: 'center'
  },
  {
    title: '所属部门',
    key: 'department',
    dataIndex: 'org.name',
    width: '',
    align: 'center'
  },
  {
    title: '手机号码',
    key: 'phone',
    dataIndex: 'phone',
    width: '',
    align: 'center'
  },
  {
    title: '邮箱',
    key: 'email',
    dataIndex: 'email',
    width: '',
    align: 'center'
  },
  {
    title: '最近登录IP',
    key: 'ip',
    dataIndex: 'last_ip',
    width: '',
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
    dataIndex: 'status',
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
        console.log(res)
        if (!res.data.status) {
          this.$message.error(res.data.msg)
          return Promise.resolve()
        }
        const { users, enabled, disabled } = res.data.data
        this.userList = users
        this.totalUser = users.length
        this.enabledUser = enabled
        this.disabledUser = disabled

        // eslint-disable-next-line camelcase
        // this.userList.last_login = moment(this.userList.last_login).format('YYYY[-]MM[-]DD HH[:]mm[:]ss')
        console.log('moment(this.userList.last_login).format(\'YYYY[-]MM[-]DD HH[:]mm[:]ss\'): ', moment(this.userList[0].last_login.substr(5, this.userList[0].last_login.length - 3)).format('YYYY[-]MM[-]DD HH[:]mm[:]ss'))
      })
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
