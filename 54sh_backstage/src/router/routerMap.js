export const routes = [
  {
    path: '/',
    name: 'base',
    redirect: () => { return '/index' }
  },
  {
    path: '/index',
    component: () => import('@/layouts/MainLayout'),
    children: [
      {
        path: '',
        name: 'index',
        component: () => import('@/pages/index')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/login')
  },
  {
    path: '/article',
    component: () => import('@/layouts/MainLayout'),
    children: [
      {
        path: 'new',
        name: 'newArticle',
        component: () => import('@/pages/article/newArticle')
      },
      {
        path: 'review',
        name: 'review',
        component: () => import('@/pages/article/review')
      },
      {
        path: 'manage',
        name: 'manageArticle',
        component: () => import('@/pages/article/manageArticle')
      }
    ]
  },
  {
    path: '/category',
    component: () => import('@/layouts/MainLayout'),
    children: [
      {
        path: 'new',
        name: 'newCategory',
        component: () => import('@/pages/category/newCategory'),
      },
      {
        path: 'manage',
        name: 'manageCategory',
        component: () => import('@/pages/category/manageCategory'),
      }
    ]
  },
  {
    path: '/tag',
    component: () => import('@/layouts/MainLayout'),
    children: [
      {
        path: 'new',
        name: 'newTag',
        component: () => import('@/pages/tag/newTag')
      },
      {
        path: 'manage',
        name: 'manageTag',
        component: () => import('@/pages/tag/manageTag')
      },
    ]
  },
  {
    path: '/user',
    component: () => import('@/layouts/MainLayout'),
    children: [
      {
        path: 'new',
        name: 'newUser',
        component: () => import('@/pages/user/newUser')
      },
      {
        path: 'manage',
        name: 'manageUser',
        component: () => import('@/pages/user/manageUser')
      }
    ]
  },
  {
    path: '*',
    name: 'error',
    component: () => import('@/pages/error')
  }
]
