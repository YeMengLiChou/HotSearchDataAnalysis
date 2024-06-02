import {createApp} from "vue";
import App from './App.vue'
import {setupRouter} from "./router";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as echarts from 'echarts'

const setupApp = async () => {
    const app = createApp(App);
    // 创建路由
    setupRouter(app);
    app.use(ElementPlus)
    app.config.globalProperties.$echarts = echarts
    app.mount('#app');

};

setupApp();
