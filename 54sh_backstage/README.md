# 升华网后台项目 - 前端

升华网后台包括 **审稿后台** 和 **网站管理** 后台

参与人员：王盛泽 周雨侬 赵文涵

### 项目技术选型

- Vue-CLI
- Vuex
- Vue-router
- Ant-Design-Vue
- SCSS
- Eslint

### 项目环境

Node.js:   12.13.0

@vue/cli:   4.5.8

### 项目结构

```
54sh_backstage
|
├-- node_modules/
├-- public
|   ├-- favicon.ico
|   └-- index.html
├-- src
|   ├-- api/            # API工厂
|   ├-- assets/         # 资源文件
|   ├-- components/     # 组件
|   ├-- layouts/        # 布局（可能只有一个文件）
|   ├-- pages/          # 页面
|   ├-- plugins/        # 插件（配置依赖）
|   ├-- router/         # 路由
|   ├-- store/          # Vuex数据源
|   ├-- App.vue
|   └-- main.js
├-- babel.config.js     # babel配置文件
├-- package.json
└-- package-lock.json
```

### 任务模块

#### 页面

- [ ] 主布局组件
- [ ] 登录页面
- [ ] 主页

#### 路由

- [ ] 配置路由
- [ ] （配置路由守卫）

#### Vuex / API工厂
