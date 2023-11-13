import { createRouter, createWebHistory } from 'vue-router';
import UserTools from '@/views/UserTools.vue';
import UserDatabases from '@/views/UserDatabases.vue';
import MainLayout from '@/views/MainLayout.vue';
import MyTools from '@/views/MyTools.vue';
import ToolDetails from '@/views/ToolDetails.vue';
import DatabaseDetails from '@/views/DatabaseDetails.vue';
import MyDatabases from '@/views/MyDatabases.vue';
import LandingPage from '@/views/LandingPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import GlobalState from '@/globalState.js';

const routes = [
    {
        path: '/',
        name: 'landingpage',
        component: LandingPage,
    },
    {
        path: '/login',
        component: LoginPage
    },
    {
        path: '/register',
        component: RegisterPage
    },
    {
        path: '/tools', // fixme: the homepage of the webapp shouldn't be /tools. Maybe later we can add a webapp home dashboard of some sort.
        component: MainLayout,
        children: [
            {
                path: '/tools',
                component: MyTools
            },
            {
                path: '/tools/:id',  // The ':id' part makes it dynamic
                name: 'tool-detail',
                component: ToolDetails,
                props: true  // This allows you to pass the dynamic segment as a prop to the component
            },
            {
                path: '/newtool',
                component: UserTools
            },
            {
                path: '/databases',
                component: MyDatabases
            },
            {
                path: '/databases/:id',  // The ':id' part makes it dynamic
                name: 'database-detail',
                component: DatabaseDetails,
                props: true  // This allows you to pass the dynamic segment as a prop to the component
            },
            {
                path: '/newdatabase',
                component: UserDatabases
            },
        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});


// This function sets a flag on sessionStorage when the page is fully loaded
window.addEventListener('load', () => {
    sessionStorage.setItem('wasPageLoaded', 'true');
});

router.beforeEach((to, from, next) => {
    // If the flag exists, we know it's a full page load
    if (sessionStorage.getItem('wasPageLoaded') === 'true') {
        GlobalState.init().then(() => {
            // Remove the flag so the next in-app navigation doesn't count as a page load
            sessionStorage.removeItem('wasPageLoaded');
            next();
        });
    } else {
        next();
    }
});

// old function to prevent constant reloading. New one above works better
// function wasPageRefreshed() {
//     const navigationEntries = performance.getEntriesByType('navigation');
//     if (navigationEntries.length > 0 && navigationEntries[0].type === 'reload') {
//         return true;
//     }
//     return false;
// }

// router.beforeEach((to, from, next) => {
//     if (wasPageRefreshed()) {
//         GlobalState.init().then(() => {
//             next();
//         });
//     } else {
//         next();  // If it's not a page refresh, just continue
//     }
// });

export default router;