export default {
  path: "/hot-search",
  redirect: "/hot-search/weibo",
  meta: {
    icon: "ri:align-item-bottom-line",
    title: "热搜数据",
    rank: 1,
    showLink: true
  },
  children: [
    {
      path: "/hot-search/weibo",
      name: "weibo",
      component: () => import("@/views/hot-search/weibo/index.vue"),
      meta: {
        title: "微博热搜榜"
      }
    },
    {
      path: "/hot-search/pengpai",
      name: "pengpai",
      component: () => import("@/views/hot-search/pengpai/index.vue"),
      meta: {
        title: "澎湃新闻"
      }
    },
    {
      path: "/hot-search/zhihu",
      name: "zhihu",
      component: () => import("@/views/hot-search/zhihu/index.vue"),
      meta: {
        title: "知乎"
      }
    },
    {
      path: "/hot-search/baidu",
      name: "baidu",
      component: () => import("@/views/hot-search/baidu/index.vue"),
      meta: {
        title: "百度"
      }
    },
    {
      path: "/hot-search/bilibili",
      name: "bilibili",
      component: () => import("@/views/hot-search/Bilibili/index.vue"),
      meta: {
        title: "哔哩哔哩"
      }
    },
    {
      path: "/hot-search/kuaishou",
      name: "kuaishou",
      component: () => import("@/views/hot-search/kuaishou/index.vue"),
      meta: {
        title: "快手"
      }
    },
    {
      path: "/hot-search/toutiao",
      name: "toutiao",
      component: () => import("@/views/hot-search/toutiao/index.vue"),
      meta: {
        title: "今日头条"
      }
    },
    {
      path: "/hot-search/tecent",
      name: "tencent",
      component: () => import("@/views/hot-search/tencent/index.vue"),
      meta: {
        title: "腾讯新闻"
      }
    },
    {
      path: "/hot-search/douyin",
      name: "douyin",
      component: () => import("@/views/hot-search/douyin/index.vue"),
      meta: {
        title: "抖音"
      }
    },
    {
      path: "/hot-search/sougou",
      name: "sougou",
      component: () => import("@/views/hot-search/sougou/index.vue"),
      meta: {
        title: "搜狗"
      }
    },
    {
      path: "/hot-search/default",
      name: "common",
      component: () => import("@/views/hot-search/default/common.vue"),
      meta: {
        title: "默认模板"
      }
    }
  ]
} satisfies RouteConfigsTable;
