import { createApp } from 'vue'
import { createPinia } from 'pinia'

import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import '@/assets/styles/main.scss'
import * as ElIconModules from '@element-plus/icons-vue'

import App from './App.vue'
import router from '@/router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import print from 'vue3-print-nb'
import VueKonva from 'vue-konva'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(print)
app.use(VueKonva)
app.use(router)


app.config.errorHandler = (err, instance, info) => {
    console.error('Global Error Caught:', err)
    console.error('Component instance:', instance)
    console.error('Error info:', info)
}


for (const [key, component] of Object.entries(ElIconModules)) {
    app.component(key, component)
}

app.mount('#app')
