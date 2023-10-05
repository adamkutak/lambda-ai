<template>
    <div class="card">
        <CreateDatabase ref="createDatabaseRef" />
    </div>
</template>

<script>
import CreateDatabase from '@/components/CreateDatabase.vue';

export default {
    components: {
        CreateDatabase,
    },
    data() {
        return {
        };
    },
}
</script>

<style scoped>
.card {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 20px;
    padding: 20px 0;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}

.CreateDatabase {
    flex: 1;
    max-width: calc(50% - 10px);
}
</style>
