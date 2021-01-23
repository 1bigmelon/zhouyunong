<template>
  <div class="container">
    <div class="form-box">
      <div class="back-box" @click="goBack">
        <a-icon type="left-circle" />
        <span>返回</span>
      </div>
      <a-alert :message="tipMessage" type="info" show-icon style="margin-bottom: .5rem;" />
      <a-spin tip="加载中..." :delay="100" size="large" :spinning="loading">
        <a-icon slot="indicator" type="loading" spin />
        <a-form class="form" :form="form" :label-col="labelCol" :wrapper-col="wrapperCol" label-align="left" @submit="submitBtnHdl">
          <a-form-item label="唯一ID">
            <a-input
              v-decorator="rules['id']"
              disabled
              allow-clear
            />
          </a-form-item>
          <a-form-item label="名称">
            <a-input
              v-decorator="rules['name']"
              placeholder="请输入新的名称"
              allow-clear
            />
          </a-form-item>
          <a-form-item label="描述">
            <a-input
              v-decorator="rules['description']"
              placeholder="请输入新的描述"
              allow-clear
            />
          </a-form-item>
          <div class="operation-box">
            <a-button type="primary" html-type="submit" :loading="submitting">提交修改</a-button>
            <a-popconfirm title="确定重置为修改前数据？" ok-text="确定" cancel-text="取消" @confirm="reset">
              <a-button type="danger">重置</a-button>
            </a-popconfirm>
          </div>
        </a-form>
      </a-spin>
    </div>
  </div>
</template>

<script>
const orgNameMap = {
  name: 'name',
  description: 'description'
}

export default {
  name: 'EditOrg',
  data() {
    return {
      // form
      labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
      },
      form: this.$form.createForm(this, { name: 'edit_org' }),
      rules: {
        id: ['id'],
        name: ['name', { rules: [
          {
            required: true,
            message: '请输入组织名称'
          }
        ] }],
        description: ['description']
      },
      submitting: false,
      tipMessage: '带红色星号的为必填，不带的为选填',
      loading: true,
      orgInfo: {}
    }
  },
  mounted() {
    this.$api.getOrgInfo(this.$route.params.id)
      .then((res) => {
        if (!res.data.status) {
          return Promise.reject(new Error(res.data.msg))
        }
        const { id, name, description } = res.data.data
        this.orgInfo = {
          id,
          name,
          description
        }
        this.form.setFieldsValue(this.orgInfo)

        this.loading = false
      }).catch((err) => {
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
          that.$router.push('/org/manage')
        }
      })
    },
    submitBtnHdl(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (err) {
          this.$message.error('请检查是否填写正确')
          return
        }

        const { name, description } = values

        const newInfo = { id: this.orgInfo.id }
        let updated = false
        for (const key in this.orgInfo) {
          if (values[key] === undefined) continue
          if (values[key] !== this.orgInfo[key]) {
            updated = true
            Object.assign(newInfo, JSON.parse(`{"${orgNameMap[key]}":"${values[key]}"}`))
          }
        }

        if (!updated) {
          this.$modal.warning({
            title: '编辑标签',
            content: '貌似没有进行修改...'
          })
          return
        }

        this.submitting = true
        this.$api.changeOrgInfo(newInfo)
          .then((res) => {
            if (!res.data.status) {
              return Promise.reject(new Error(res.data.msg))
            }

            this.$message.success('组织信息修改成功')
            this.$router.push('/org/manage')
          })
          .catch((err) => {
            this.$message.error(err.message)
          })
          .finally(() => {
            this.submitting = false
          })
      })
    },
    reset() {
      this.form.setFieldsValue(this.orgInfo)
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
