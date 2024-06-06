import type { App } from 'vue';
import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
// 引入测试页面
import defaultPage from './modules/default'
import weiboPage from './modules/weibo'
import baiduPage from './modules/baidu'
import pengpai from "./modules/pengpai";
import sougou from "./modules/sougou";
import toutiao from "./modules/toutiao";
import zhihu from "./modules/zhihu";
export const publicRoutes: Array<RouteRecordRaw> = [
    ...defaultPage,
    ...weiboPage,
    ...toutiao,
    ...sougou,
    ...pengpai,
    ...zhihu,
    ...baiduPage,
];

const router = createRouter({
    history: createWebHashHistory(),
    routes: publicRoutes
});

/* 初始化路由表 */
export function resetRouter() {
    router.getRoutes().forEach((route) => {
        const { name } = route;
        if (name) {
            router.hasRoute(name) && router.removeRoute(name);
        }
    });
}
/* 导出 setupRouter */
export const setupRouter = (app: App<Element>) => {
    app.use(router);
};
