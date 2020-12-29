<template>
  <div class="container">
    <div class="form-box">
      <a-alert :message="tipMessage" type="info" show-icon style="margin-bottom: .5rem;" />
      <a-form class="form" :form="form" :label-col="labelCol" :wrapper-col="wrapperCol" label-align="left" @submit="submitBtnHdl">
        <a-form-item label="名称">
          <a-input
            v-decorator="rules['name']"
            placeholder="请输入名称"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="描述">
          <a-input
            v-decorator="rules['description']"
            placeholder="请输入描述"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="所属分类">
          <a-select
            v-decorator="rules['category']"
            placeholder="请选择所属分类"
          >
            <a-select-option v-for="(item, index) in categoryList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="所属组织">
          <a-select
            v-decorator="rules['organization']"
            placeholder="请选择所属部门"
          >
            <a-select-option v-for="(item, index) in orgList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-item>
        <div class="submit-box">
          <a-button type="primary" html-type="submit" :loading="submitting">创建标签</a-button>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NewTag',
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
        name: ['name', { rules: [
          {
            required: true,
            message: '请输入标签名称'
          }
        ] }],
        description: ['description'],
        category: ['category', { rules: [
          {
            required: true,
            message: '请选择所属分类'
          }
        ] }],
        organization: ['organization', { rules: [
          {
            required: true,
            message: '请选择标签所属部门'
          }
        ] }]
      },
      orgList: [],
      categoryList: [],
      submitting: false,
      tipMessage: '带红色星号的为必填，不带的为选填'
    }
  },
  mounted() {
    Promise.all([this.$api.getAllOrgs(), this.$api.getAllCategories()])
      .then((res) => {
        res.forEach((item) => {
          if (!item.data.status) {
            return Promise.reject(new Error(item.data.msg))
          }
        })
        this.orgList = res[0].data.data.orgs

        this.categoryList = res[1].data.data.divs
      })
      .catch((err) => {
        this.$message.error(err.message)
      })
  },
  methods: {
    submitBtnHdl(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (err) {
          this.$message.errpr(err)
          return
        }

        this.submitting = true
        const { name, description, organization } = values
        this.$api.createTag({
          name,
          org: organization,
          description,
          color: 'pink'
        }).then((res) => {
          if (!res.data.status) {
            return Promise.reject(new Error(res.data.msg))
          }

          this.$message.success('标签创建成功')
          this.$router.push('/tag/manage')
        }).catch((err) => {
          this.$message.error(err.message)
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
