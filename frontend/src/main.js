import { createApp } from 'vue'
import router from './router'
import naive from './naive'
import App from './App.vue'
const app = createApp(App)

app.use(router)
app.use(naive)

app.mount('#app')
