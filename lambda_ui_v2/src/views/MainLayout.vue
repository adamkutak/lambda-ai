<template>
    <div class="layout-container">
        <MainSidebar class="main-sidebar"/>
        <div class="main-content">
            <router-view />
        </div>
    </div>
</template>

<script>
import MainSidebar from '@/components/MainSidebar.vue';

export default {
    components: {
        MainSidebar,
    }
}
</script>

<style scoped>
.layout-container {
    display: flex;
    height: 100%;
    /* Set to flex to align children horizontally */
}

.main-content {
    flex-grow: 1;
    padding-left: 20px;
}

.main-sidebar {
    height: 100vh;
}
</style>
