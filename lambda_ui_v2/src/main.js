import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import GlobalState from '@/globalState.js';
import axios from 'axios';

axios.defaults.withCredentials = true;

createApp(App).use(router).mount('#app');

GlobalState.init();