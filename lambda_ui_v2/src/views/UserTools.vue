<template>
    <div class="card">
        <CreateTool ref="createToolRef" :testCases="testCasesData" @update:selectedDatabase="handleDatabaseUpdate"/>
        <TestCases ref="testCasesRef" :inputs="inputs" :outputs="outputs" :selectedDatabase="selectedDatabase"/>
    </div>
</template>
  
<script>
import CreateTool from '@/components/CreateTool.vue';
import TestCases from '@/components/TestCases.vue';

export default {
    components: {
        CreateTool,
        TestCases
    },
    data() {
        return {
            inputs: [],
            outputs: [],
            selectedDatabase: null,
            testCasesData: []
        };
    },
    mounted() {
        if (this.$refs.createToolRef) {
            this.inputs = this.$refs.createToolRef.tool.inputs;
            this.outputs = this.$refs.createToolRef.tool.outputs;
            this.selectedDatabase = this.$refs.createToolRef.tool.selectedDatabase;
        }
        if (this.$refs.testCasesRef) {
            this.testCasesData = this.$refs.testCasesRef.testCases;
        }
    },
    methods: {
        handleDatabaseUpdate(newDatabase) {
            this.selectedDatabase = newDatabase;
        }
    }
}
</script>

  
<style scoped>
.card {
    display: flex;
    justify-content: center;
    /* Centers child components horizontally */
    align-items: flex-start;
    /* Aligns child components to the top */
    gap: 20px;
    /* Gap between child components */
    padding: 20px 0;
    /* Padding at the top and bottom */
    width: 100%;
    max-width: 1200px;
    /* Optional max-width for wider screens */
    margin: 0 auto;
    /* Centers the card on the page */
}

.CreateTool,
.TestCases {
    flex: 1;
    /* Each child takes up equal width */
    max-width: calc(50% - 10px);
    /* Optional: Ensures that with the gap, each child is not more than half the container width */
}
</style>
