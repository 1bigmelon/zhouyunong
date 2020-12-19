<template>
  <div class="container">
    <div class="form-box">
      <a-alert :message="tipMessage" type="info" show-icon style="margin-bottom: .5rem;" />
      <a-form class="form" :form="form" :label-col="labelCol" :wrapper-col="wrapperCol" label-align="left" @submit="submitBtnHdl">
        <a-form-item label="用户名">
          <a-input
            v-decorator="rules['username']"
            placeholder="请输入用户名"
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="真实姓名">
          <a-input
            v-decorator="rules['realname']"
            placeholder="请输入真实姓名"
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="密码">
          <a-input-password
            v-decorator="rules['firstPwd']"
            placeholder="请输入密码"
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
            placeholder="请输入固定电话"
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="手机号码">
          <a-input
            v-decorator="rules['cellPhone']"
            placeholder="请输入手机号码"
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="邮箱">
          <a-input
            v-decorator="rules['email']"
            placeholder="请输入邮箱"
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="权限角色">
          <a-select
            v-decorator="rules['role']"
            placeholder="请选择权限角色"
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
            placeholder="请选择所属部门"
          >
            <a-select-option v-for="(item, index) in orgList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-item>
        <div class="submit-box">
          <a-button type="primary" html-type="submit" :loading="submitting">创建用户</a-button>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NewUser',
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
        username: [
          'username',
          {
            rules: [
              {
                required: true,
                message: '请输入用户名'
              }
            ]
          }
        ],
        realname: [
          'realname',
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
                required: true,
                message: '请输入密码!'
              },
              {
                min: 6,
                message: '请输入至少6位密码!'
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
                required: true,
                message: '请输入与上面一致的密码!',
              },
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
                message: '请输入手机号码!'
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
                message: '请输入正确的电子邮箱!',
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
                message: '请选择权限角色!'
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
                message: '请选择所属部门!'
              }
            ]
          }
        ]
      },
      validPwd: false,
      orgList: [],
      submitting: false,
      tipMessage: '带红色星号的为必填，不带的为选填'
    }
  },
  mounted() {
    this.$api.getAllOrgs()
      .then((res) => {
        if (!res.data.status) {
          this.$message.error(res.data.msg)
          return Promise.resolve()
        }
        this.orgList = res.data.data.orgs
      })
  },
  methods: {
    validateFirstPassword(rule, value, callback) {
      if (value && this.validPwd) {
        this.form.validateFields(['confirm'], { force: true })
      }
      callback()
    },
    validateSecondPassword(rule, value, callback) {
      if (value && value !== this.form.getFieldValue('password')) {
        callback('两次输入的密码不一致!')
      }
      else {
        callback()
      }
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

        this.submitting = true
        this.$api.createUser({
          name: values.realname,
          // eslint-disable-next-line camelcase
          user_id: values.username,
          password: values.password,
          tel: values.fixedPhone,
          phone: values.cellPhone,
          email: values.email,
          role: values.role,
          org: values.department
        }).then((res) => {
          if (!res.data.status) {
            throw new Error(res.data.msg)
          }

          this.$message.success('用户创建成功！')
          this.$router.push('/user/manage')
        }).catch((err) => {
          this.$message.error(err)
        }).finally(() => {
          this.submitting = false
        })
      })
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

      .form {
        width: 25rem;
        margin-top: .8rem;

        .submit-box {
          display: flex;
          justify-content: center;

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
