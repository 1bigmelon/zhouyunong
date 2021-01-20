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
          <a-form-item label="所属分类">
            <a-select
              v-decorator="rules['category']"
              placeholder="请选择新的所属分类"
            >
              <a-select-option v-for="(item, index) in categoryList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="所属组织">
            <a-select
              v-decorator="rules['organization']"
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
      </a-spin>
    </div>
  </div>
</template>

<script>
const tagNameMap = {
  name: 'name',
  description: 'description',
  category: 'category',
  organization: 'org'
}

export default {
  name: 'EditTag',
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
      form: this.$form.createForm(this, { name: 'new_user' }),
      rules: {
        id: ['id'],
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
      tipMessage: '带红色星号的为必填，不带的为选填',
      loading: true,
      tagInfo: {}
    }
  },
  mounted() {
    Promise.all([
      this.$api.getTagInfo(this.$route.params.id),
      this.$api.getAllOrgs(),
      this.$api.getAllCategories()
    ]).then((res) => {
      res.forEach((item) => {
        if (!item.data.status) {
          return Promise.reject(new Error(item.data.msg))
        }
      })
      const { id, name, description, org } = res[0].data.data
      this.tagInfo = {
        id,
        name,
        description,
        organization: org.name
      }
      this.form.setFieldsValue(this.tagInfo)

      this.orgList = res[1].data.data.orgs

      this.categoryList = res[2].data.data.divs

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
          that.$router.push('/tag/manage')
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

        const { name, description, organization } = values

        const newInfo = { id: this.tagInfo.id }
        let updated = false
        for (const key in this.tagInfo) {
          if (values[key] === undefined) continue
          if (values[key] !== this.tagInfo[key]) {
            updated = true
            Object.assign(newInfo, JSON.parse(`{"${tagNameMap[key]}":"${values[key]}"}`))
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
        this.$api.changeTagInfo(newInfo)
          .then((res) => {
            if (!res.data.status) {
              return Promise.reject(new Error(res.data.msg))
            }

            this.$message.success('标签信息修改成功')
            this.$router.push('/tag/manage')
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
      this.form.setFieldsValue(this.tagInfo)
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
