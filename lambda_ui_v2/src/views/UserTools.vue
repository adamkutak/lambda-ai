<template>
    <div class="container">
        <CreateTool ref="createToolRef" />
        <TestCases :inputs="inputs" :outputs="outputs" />
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
            outputs: []
        };
    },
    mounted() {
        if (this.$refs.createToolRef) {
            this.inputs = this.$refs.createToolRef.tool.inputs;
            this.outputs = this.$refs.createToolRef.tool.outputs;
        }
    }
}
</script>
  
<style scoped>
.container {
    display: flex;
    gap: 20px;
    /* or whatever gap you'd like between the components */
}

.CreateTool,
.TestCases {
    flex: 1;
}
</style>
