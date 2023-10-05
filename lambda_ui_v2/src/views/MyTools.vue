<template>
    <div class="tools-page">
        <div class="header">
            <h1>Tools</h1>
            <router-link to="/newtool" class="create-btn">Create New</router-link>
        </div>
        <div class="tools-container">
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Inputs</th>
                        <th>Outputs</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="row in tableRows">
                        <tr @click="toggleDetails(row.id)" v-if="!row.isDetailRow" :key="row.id">
                            <td>{{ row.name }}</td>
                            <td>{{ row.inputs.join(', ') }}</td>
                            <td>{{ row.outputs.join(', ') }}</td>
                            <td><router-link :to="'/tools/' + row.id">View</router-link></td>
                        </tr>
                        <tr v-if="row.isDetailRow" :key="'details-' + row.id">
                            <td colspan="4">{{ row.description }}</td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            tools: [
                {
                    id: 1,
                    name: "Tool 1",
                    inputs: ["input1", "input2"],
                    outputs: ["output1", "output2"],
                    description: "This is a description for Tool 1.",
                    showDetails: false
                },
                {
                    id: 2,
                    name: "Tool 2",
                    inputs: ["input10", "input200"],
                    outputs: ["output100", "output2000"],
                    description: "My new tool is even better than the first one.",
                    showDetails: false
                },
            ]
        };
    },
    computed: {
        tableRows() {
            const rows = [];
            this.tools.forEach(tool => {
                rows.push(tool);
                if (tool.showDetails) {
                    rows.push({ ...tool, isDetailRow: true });
                }
            });
            return rows;
        }
    },
    methods: {
        toggleDetails(id) {
            const tool = this.tools.find(t => t.id === id);
            if (tool) tool.showDetails = !tool.showDetails;
        }
    }
}

</script>
  
<style scoped>
.tools-page {
    padding: 10px;
    font-family: 'Arial', sans-serif;
    background-color: #f5f5f5;
}

.header {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    /* To position the button absolutely relative to this container */
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 1;
}

.tools-container {
    overflow-y: auto;
    height: 90vh;
    border-radius: 5px;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-height: calc(100vh - 119px);
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 0;
}

th,
td {
    padding: 10px 15px;
    border: 1px solid #ddd;
}

th {
    background-color: #f0f0f0;
}

tr:hover {
    background-color: #e0e0e0;
}

.router-link {
    text-decoration: none;
    color: #3498db;
    transition: color 0.3s ease;
}

router-link:hover {
    color: #2c3e50;
}

.create-btn {
    position: absolute;
    right: 20px;
    /* 20px from the right edge */
    padding: 10px 20px;
    background-color: #3498db;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    text-decoration: none;
}

.create-btn:hover {
    background-color: #2980b9;
}
</style>