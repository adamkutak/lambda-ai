<template>
    <div class="layout-container">
        <MainSidebar />
        <div class="main-content">
            <router-view />
        </div>
    </div>
</template>

<script>
import MainSidebar from '@/components/MainSidebar.vue';  // Updated to MainSidebar

export default {
    components: {
        MainSidebar  // Updated to MainSidebar
    }
}
</script>

<style scoped>
.layout-container {
    display: flex;
    /* Set to flex to align children horizontally */
}

.main-content {
    flex-grow: 1;
    padding-left: 20px;
}
</style>
