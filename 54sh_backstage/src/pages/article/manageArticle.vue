<template>
  <div class="container">
    <!-- <div class="greeting-box">
      <span>{{ greeting }}，</span>
      <span>{{ userInfo.name }}</span>
    </div> -->
    <div class="data-box">
      <data-box icon="file-text" title="文章总数量" :value="1564" />
      <data-box icon="file-protect" title="待二审数量" :value="745" />
      <data-box icon="audit" title="待终审数量" :value="545" />
      <data-box icon="cloud-upload" title="待发布数量" :value="976" />
      <data-box icon="cloud" title="已发布数量" :value="432" />
      <data-box icon="delete" title="回收站数量" :value="15" />
    </div>
    <div class="content-box">
      <div class="search-box">
      </div>
      <div class="high-height-list-box">
        <a-table :columns="columns" :data-source="test" row-key="id">
          <template slot="tag" slot-scope="tags">
            <a-tag
              v-for="(item, index) in tags"
              :key="index"
              :color="color[Math.floor(Math.random() * color.length)]"
              style="width: 6rem; display: block; margin: .3rem auto;"
            >
              <a-tooltip>
                <template slot="title">{{ item }}</template>
                <span>{{ tagText(item) }}</span>
              </a-tooltip>
            </a-tag>
          </template>
          <template slot="operation" style="operation-box">
            <a-button type="primary" size="small" style="font-size: .7rem; margin-right: .5rem;">编辑</a-button>
            <a-button type="danger" size="small" style="font-size: .7rem;">删除</a-button>
          </template>
        </a-table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import DataBox from '@/components/DataBox.vue'
import moment from 'moment'

const columns = [{
  title: 'ID',
  key: 'id',
  dataIndex: 'id',
  width: '4%',
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
  width: '8%',
  align: 'center'
},
{
  title: '文章标签',
  key: 'tag',
  dataIndex: 'tag',
  width: '9%',
  align: 'center',
  scopedSlots: { customRender: 'tag' }
},
{
  title: '文章所属组织',
  key: 'org',
  dataIndex: 'org',
  width: '11%',
  align: 'center'
},
{
  title: '时间',
  key: 'time',
  dataIndex: 'time',
  width: '8%',
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
  width: '10%',
  align: 'center',
  scopedSlots: { customRender: 'operation' }
}]

const color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']

export default {
  name: 'ManageArticle',
  components: {
    DataBox
  },
  data() {
    return {
      greeting: '',
      columns,
      color,
      colorUsed: '',
      test: [
        {
          id: 1,
          title: '中南大学党校第41期入党积极分子暨第10期发展对象培训班（计算机学院分校第4期培训班）结业典礼顺利举行',
          category: '	团学资讯',
          tag: ['百千万阳光关心志愿者行动计划', '我的返家乡实践故事'],
          org: '数学与统计学院',
          time: '',
          status: '已发布'
        },
        {
          id: 451,
          title: '“学习党的十九届五中全会精神”主题党课',
          category: '测试分类',
          tag: ['标签1'],
          org: '交通运输工程学院',
          time: '',
          status: '二审未通过'
        },
        {
          id: 9999,
          title: '测试标题',
          category: '测试分类',
          tag: [],
          org: '地球科学与信息物理学院',
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
    const hour = moment().hour()
    if (hour >= 6 && hour < 9) this.greeting = '早上好'
    if (hour >= 9 && hour < 11) this.greeting = '上午好'
    if (hour >= 11 && hour < 13) this.greeting = '中午好'
    if (hour >= 13 && hour < 19) this.greeting = '下午好'
    if (hour >= 19 || hour < 6) this.greeting = '晚上好'

    this.test.forEach((item) => {
      item.time = moment().format('YYYY[-]MM[-]DD HH:mm:ss')
    })
  },
  methods: {
    tagText(text) {
      if (text.length >= 6) {
        text = text.substr(0, 6)
        text += '...'
      }
      return text
    }
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
        transform: translateY(2rem);
      }
    }

    .data-box {
      @extend .data-box;
      width: 100%;
    }

    .content-box {
      @extend .component;
      margin-top: 1.5rem;
      width: 100%;

      .search-box {
        height: 10rem;
        width: 100%;
        background-color: pink;
      }
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
