<template>
  <div class="container">
    <div class="form-box">
      <div class="back-box" @click="goBack">
        <a-icon type="left-circle" />
        <span>返回</span>
      </div>
      <a-alert :message="tipMessage" type="info" show-icon style="margin-bottom: .5rem;" />
      <a-form class="form" :form="form" :label-col="labelCol" :wrapper-col="wrapperCol" label-align="left" @submit="submitBtnHdl">
        <a-form-item label="唯一ID">
          <a-input
            v-decorator="rules['id']"
            disabled
            allow-clear
          />
        </a-form-item>
        <a-form-item label="用户名">
          <a-input
            v-decorator="rules['username']"
            placeholder="请输入新的用户名"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="真实姓名">
          <a-input
            v-decorator="rules['name']"
            placeholder="请输入新的真实姓名"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="密码">
          <a-input-password
            v-decorator="rules['firstPwd']"
            placeholder="若不改变密码则无需填写"
            allow-clear
            @blur="inputBlurHdl"
          ></a-input-password>
        </a-form-item>
        <a-form-item label="再次确认密码">
          <a-input-password
            v-decorator="rules['secondPwd']"
            placeholder="请输入与上面一致的密码"
            allow-clear
          ></a-input-password>
        </a-form-item>
        <a-form-item label="固定电话">
          <a-input
            v-decorator="rules['fixedPhone']"
            placeholder="请输入新的固定电话"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="手机号码">
          <a-input
            v-decorator="rules['cellPhone']"
            placeholder="请输入新的手机号码"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="邮箱">
          <a-input
            v-decorator="rules['email']"
            placeholder="请输入新的邮箱"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="权限角色">
          <a-select
            v-decorator="rules['role']"
            placeholder="请选择新的权限角色"
          >
            <a-select-option key="FirstAudit" value="一审">一审</a-select-option>
            <a-select-option key="SecondAudit" value="二审">二审</a-select-option>
            <a-select-option key="FinalAudit" value="终审">终审</a-select-option>
            <a-select-option key="Admin" value="管理员">管理员</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="所属部门">
          <a-select
            v-decorator="rules['department']"
            placeholder="请选择新的所属部门"
          >
            <a-select-option v-for="(item, index) in orgList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-item>
        <div class="operation-box">
          <a-button type="primary" html-type="submit" :loading="submitting">提交修改</a-button>
          <a-popconfirm title="确定重置为修改前数据？" ok-text="确定" cancel-text="取消" @confirm="reset">
            <a-button type="danger">重置</a-button>
          </a-popconfirm>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script>
/* eslint-disable camelcase */

const userInfoMap = {
  username: 'user_id',
  name: 'name',
  fixedPhone: 'tel',
  cellPhone: 'phone',
  department: 'org'
}

export default {
  name: '',
  data() {
    return {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
      },
      form: this.$form.createForm(this, { name: 'new_user' }),
      rules: {
        id: ['id'],
        username: ['username', { rules: [
          {
            required: true,
            message: '请输入用户名'
          }]
        }],
        name: [
          'name',
          {
            rules: [
              {
                required: true,
                message: '请输入真实姓名'
              }
            ]
          }
        ],
        firstPwd: [
          'password',
          {
            rules: [
              {
                min: 6,
                message: '请输入至少6位密码'
              },
              {
                validator: this.validateFirstPassword,
              },
            ],
          },
        ],
        secondPwd: [
          'confirm',
          {
            rules: [
              {
                validator: this.validateSecondPassword,
              },
            ],
          },
        ],
        fixedPhone: ['fixedPhone'],
        cellPhone: [
          'cellPhone',
          {
            rules: [
              {
                required: true,
                message: '请输入手机号码'
              },
              {
                len: 11,
                message: '请输入正确的手机号码'
              }
            ],
          },
        ],
        email: [
          'email',
          {
            rules: [
              {
                type: 'email',
                message: '请输入正确的电子邮箱',
              }
            ],
          },
        ],
        role: [
          'role',
          {
            rules: [
              {
                required: true,
                message: '请选择权限角色'
              }
            ]
          }
        ],
        department: [
          'department',
          {
            rules: [
              {
                required: true,
                message: '请选择所属部门'
              }
            ]
          }
        ]
      },
      validPwd: false,
      orgList: [],
      submitting: false,
      tipMessage: '带红色星号的为必填，不带的为选填',
      userInfo: {}
    }
  },
  mounted() {
    this.$api.getUserInfo(this.$route.params.username)
      .then((res) => {
        if (!res.data.status) {
          this.$message.error(res.data.msg)
          return Promise.resolve()
        }
        const { id, user_id, name, tel, phone, email, role, org } = res.data.data
        this.userInfo = {
          id,
          username: user_id,
          name,
          fixedPhone: tel,
          cellPhone: phone,
          email,
          role,
          department: org.name
        }
        this.form.setFieldsValue({
          id,
          username: user_id,
          name,
          fixedPhone: tel,
          cellPhone: phone,
          email,
          role,
          department: org.name
        })
      })
      .catch((err) => {
        this.$message.error(err.message)
      })

    this.$api.getAllOrgs()
      .then((res) => {
        if (!res.data.status) {
          this.$message.error(res.data.msg)
          return Promise.resolve()
        }
        this.orgList = res.data.data.orgs
      })
      .catch((err) => {
        this.$message.error(err.message)
      })
  },
  methods: {
    goBack() {
      const that = this
      this.$modal.confirm({
        title: '确定离开此页面？',
        content: '在该页面上所做的更改不会保存！',
        okText: '确定',
        cancelText: '取消',
        onOk() {
          that.$router.push('/user/manage')
        },
        onCancel() {}
      })
    },
    inputBlurHdl(e) {
      const value = e.target.value
      this.validPwd = (value && value.length >= 6)
    },
    submitBtnHdl(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (err) {
          this.$message.error(err)
          return
        }

        const newInfo = { id: this.userInfo.id }
        let updated = false
        for (const key in this.userInfo) {
          if (values[key] === undefined) continue
          if (values[key] !== this.userInfo[key]) {
            updated = true
            Object.assign(newInfo, JSON.parse(`{"${userInfoMap[key]}":"${values[key]}"}`))
          }
        }
        if (values.password) {
          updated = true
          Object.assign(newInfo, { password: values.password })
        }
        if (!updated) {
          this.$modal.warning({
            title: '编辑用户',
            content: '貌似没有进行修改...'
          })
          return
        }

        this.submitting = true
        this.$api.changeUserInfo(newInfo)
          .then((res) => {
            if (!res.data.status) {
              return Promise.reject(res.data.msg)
            }

            this.$message.success('用户信息修改成功')
            this.$router.push('/user/manage')
          })
          .catch((err) => {
            this.$message.error(err?.data.msg)
          })
          .finally(() => {
            this.submitting = false
          })
      })
    },
    reset() {
      this.form.setFieldsValue(this.userInfo)
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;

    .form-box {
      @extend .component;

      width: 42rem;
      padding: 2rem {
        bottom: 3rem;
      };
      display: flex;
      align-items: center;
      flex-direction: column;
      position: relative;

      .back-box {
        position: absolute;
        left: 3rem;
        top: 2.3rem;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        transition: all .2s ease;

        &:hover {
          cursor: pointer;
          color: $theme-color;
          transition: all .2s ease;
        }

        span {
          margin-left: .5rem;
        }
      }

      .form {
        width: 25rem;
        margin-top: .8rem;

        .operation-box {
          display: flex;
          justify-content: space-around;
          padding: 0 1rem;

          button {
            width: 30%;
            height: 2.5rem;
            font-size: 14px;
            margin-top: .8rem;
          }
        }
      }
    }
  }
</style>
