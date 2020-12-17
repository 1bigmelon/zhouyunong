<template>
  <div class="container">
    <div class="form-box">
      <a-alert :message="tipMessage" type="info" show-icon style="margin-bottom: .5rem;" />
      <a-form class="form" :form="form" :label-col="labelCol" :wrapper-col="wrapperCol" label-align="left" @submit="submitBtnHdl">
        <a-form-item label="唯一ID">
          <a-input
            v-decorator="rules['uid']"
            disabled
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="用户名">
          <a-input
            v-decorator="rules['username']"
            placeholder="请输入新的用户名"
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="真实姓名">
          <a-input
            v-decorator="rules['realname']"
            placeholder="请输入新的真实姓名"
            allow-clear
          ></a-input>
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
          ></a-input>
        </a-form-item>
        <a-form-item label="手机号码">
          <a-input
            v-decorator="rules['cellPhone']"
            placeholder="请输入新的手机号码"
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="邮箱">
          <a-input
            v-decorator="rules['email']"
            placeholder="请输入新的邮箱"
            allow-clear
          ></a-input>
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
        <div class="submit-box">
          <a-button type="primary" html-type="submit" :loading="submitting">提交修改</a-button>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script>
/* eslint-disable camelcase */

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
        uid: [
          'uid'
        ],
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
        this.userInfo = { id, user_id, name, tel, phone, email, role, org }
        this.form.setFieldsValue({
          uid: id,
          username: user_id,
          realname: name,
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
    inputBlurHdl(e) {
      const value = e.target.value
      this.validPwd = (value && value.length >= 6)
    },
    submitBtnHdl(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        /** TODO:
         *  判断更新
         */

        if (err) {
          this.$message.error(err)
          return
        }

        this.submitting = true

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
