<template>
  <div class="container">
    <div class="greeting-box">
      <span>{{ greeting }}，</span>
      <span>{{ userInfo.name }}</span>
    </div>
    <div class="data-box">
      <data-box icon="file-text" title="文章总数量" :value="1564" />
      <data-box icon="file-protect" title="待二审数量" :value="745" />
      <data-box icon="cloud" title="已发布数量" :value="432" />
      <data-box icon="audit" title="待终审数量" :value="545" />
      <data-box icon="cloud-upload" title="待发布数量" :value="976" />
      <data-box icon="delete" title="回收站数量" :value="15" />
    </div>
    <div class="content-box">
      <div class="search-box">

      </div>
      <div class="list-box">
        <a-table :columns="columns" :data-source="test">
          <template slot="tag" slot-scope="tags">
            <div v-for="(item, index) in tags" :key="index">{{ item }}</div>
          </template>
        </a-table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import DataBox from '../components/DataBox.vue'

const columns = [{
  title: 'ID',
  key: 'id',
  dataIndex: 'id',
  width: '6%',
  align: 'center'
},
{
  title: '文章标题',
  key: 'title',
  dataIndex: 'title'
},
{
  title: '文章分类',
  key: 'category',
  dataIndex: 'category',
  width: '10%',
  align: 'center'
},
{
  title: '文章标签',
  key: 'tag',
  dataIndex: 'tag',
  width: '13%',
  align: 'center',
  scopedSlots: { customRender: 'tag' }
},
{
  title: '文章所属组织',
  key: 'org',
  dataIndex: 'org',
  width: '13%',
  align: 'center'
},
{
  title: '时间',
  key: 'time',
  dataIndex: 'time',
  width: '14%',
  align: 'center'
},
{
  title: '当前状态',
  key: 'status',
  dataIndex: 'status',
  width: '8%',
  align: 'center'
},
{
  title: '操作',
  key: 'operation',
  dataIndex: '',
  width: '10%',
  align: 'center'
}]

export default {
  name: 'Index',
  components: {
    'data-box': DataBox
  },
  data() {
    return {
      greeting: '',
      columns,
      test: [
        {
          id: 9999,
          title: '测试标题',
          category: '测试分类',
          tag: ['测试标签1', '测试标签2'],
          org: '测试组织',
          time: '',
          status: '已发布'
        }
      ]
    }
  },
  computed: {
    ...mapState(['userInfo'])
  },
  mounted() {
    const hour = new Date().getHours()
    if (hour >= 6 && hour < 9) this.greeting = '早上好'
    if (hour >= 9 && hour < 11) this.greeting = '上午好'
    if (hour >= 11 && hour < 13) this.greeting = '中午好'
    if (hour >= 13 && hour < 19) this.greeting = '下午好'
    if (hour >= 19 || hour < 6) this.greeting = '晚上好'

    this.test[0].time = `${new Date().toISOString().substr(0, 10)} ${new Date().getHours()}:${new Date().getMinutes()}:${new Date().getSeconds()}`
  }
}
</script>

<style lang="scss" scoped>
  .container {
    height: 100%;
    width: 100%;
    display: block;

    .greeting-box {
      height: 1.8rem;
      min-width: 100%;
      margin-bottom: 1.7rem;
      overflow: hidden;

      span {
        display: inline-block;
      }

      span:nth-child(1) {
        font-size: 1.1rem;
        margin-left: 1rem;
        animation: greeting-show .8s ease;
      }

      span:nth-child(2) {
        font-size: 1.4rem;
        animation: greeting-show .8s ease .3s;
        animation-fill-mode: forwards;
        transform: translateY(1.8rem);
      }
    }

    .data-box {
      min-width: 100%;
      display: flex;
      justify-content: space-around;
    }

    .content-box {
      @extend .component;

      margin-top: 1.5rem;
      width: 100%;
    }
  }

  @keyframes greeting-show {
    from {
      transform: translateY(1.8rem);
    }

    to {
      transform: translateY(0);
    }
  }
</style>
