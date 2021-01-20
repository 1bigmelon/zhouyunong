<template>
  <div class="container">
    <div class="form-box">
      <a-form class="form" :form="form" :label-col="labelCol" :wrapper-col="wrapperCol" label-align="left" @submit="submitBtnHdl">
        <a-form-item label="分类总署">
          <a-select
            v-decorator="rules['role']"
            placeholder="请选择分类总署"
          >
            <a-select-option key="department" value="校团委部门">校团委部门</a-select-option>
            <a-select-option key="column" value="校团委专栏">校团委专栏</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="名称">
          <a-input
            v-decorator="rules['categoryName']"
            placeholder="请输入名称"
            allow-clear
          ></a-input>
        </a-form-item>
        <a-form-item label="所属组织">
          <a-select
            v-decorator="rules['organization']"
            placeholder="请选择所属组织"
          >
            <a-select-option v-for="(item, index) in orgList" :key="index" :value="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="描述">
          <a-input
            v-decorator="rules['description']"
            placeholder="请输入描述"
            allow-clear
          ></a-input>
        </a-form-item>
        <div class="submit-box">
          <a-button type="primary" html-type="submit" :loading="submitting">新建分类</a-button>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NewCateg',
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
      form: this.$form.createForm(this, { name: 'new_category' }),
      rules: {
        headquarters: [
          'headquarters',
          {
            rules: [
              {
                required: true,
                massage: '请选择分类总署'
              }
            ]
          }
        ],
        categroyName: [
          'categroyName',
          {
            rules: [
              {
                required: true,
                massage: '请输入名称'
              }
            ]
          }
        ],
        description: [
          'description',
          {
            rules: [
              {
                ruquired: true,
                massage: '请输入描述'
              }
            ]
          }
        ],
        organization: [
          'organization',
          {
            rules: [
              {
                ruquired: true,
                massage: '请输入所属组织'
              }
            ]
          }
        ]
      },
      orgList: [],
      submitting: false
    }
  },
  mounted() {
    this.$api.getAllOrgs()
      .then((res) => {
        if (!res.data.status) {
          this.$message.error(res.data.msg)
          return Promise.resolve()
        }
        console.log(res)
        this.orgList = res.data.data.orgs
      })
  },
  methods: {
    submitBtnHdl(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (err) {
          this.$message.error('请检查是否填写正确')
          return
        }

        this.submitting = true
        this.$api.createCategory({
          name: values.categroyName,
          org: values.organization,
          description: values.description,
        }).then((res) => {
          this.submitting = false

          if (!res.data.status) {
            this.$message.error(res.data.msg)
            return Promise.resolve()
          }

          this.$message.success('分类创建成功！')
          this.$router.push('/category/manage')
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
    justify-content:center;
    align-items: center;

    .form-box {
      @extend .component;
      width: 55%;
      padding: 2rem{
          bottom: 3rem;
      };

      display: flex;
      justify-content: center;

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
