export default {
  path: "/hot-search",
  redirect: "/hot-search/weibo",
  meta: {
    icon: "ri:information-line",
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
      path: "/hot-search/default",
      name: "default",
      component: () => import("@/views/hot-search/default/index.vue"),
      meta: {
        title: "默认模板"
      }
    }
  ]
} satisfies RouteConfigsTable;
