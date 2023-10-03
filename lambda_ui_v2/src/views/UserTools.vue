<template>
    <div class="card">
        <CreateTool ref="createToolRef" :testCases="testCasesData" />
        <TestCases ref="testCasesRef" :inputs="inputs" :outputs="outputs" />
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
            testCasesData: []
        };
    },
    mounted() {
        if (this.$refs.createToolRef) {
            this.inputs = this.$refs.createToolRef.tool.inputs;
            this.outputs = this.$refs.createToolRef.tool.outputs;
        }
        if (this.$refs.testCasesRef) {
            this.testCasesData = this.$refs.testCasesRef.testCases;
        }
    }
}
</script>

  
<style scoped>
.card {
    display: flex;
    gap: 20px;
    /* or whatever gap you'd like between the components */
}

.CreateTool,
.TestCases {
    flex: 1;
}
</style>
