import { createRouter, createWebHistory } from 'vue-router';
import HomeFirst from '@/views/HomeFirst.vue';
import UserTools from '@/views/UserTools.vue';
import UserDatabases from '@/views/UserDatabases.vue';
import MainLayout from '@/views/MainLayout.vue';


const routes = [
    {
        path: '/',
        redirect: '/tools',  // Redirect root to /tools by default
        component: MainLayout,
        children: [
            {
                path: 'tools',
                component: UserTools
            },
            {
                path: 'databases',
                component: UserDatabases
            }
        ]
    },
    {
        path: '/home',
        name: 'HomeFirst',
        component: HomeFirst
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;