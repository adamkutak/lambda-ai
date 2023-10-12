import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import GlobalState from '@/globalState.js';

createApp(App).use(router).mount('#app');

GlobalState.init();