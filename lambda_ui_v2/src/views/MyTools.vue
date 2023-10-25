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
                    <template v-for="tool in tools" :key="tool.id">
                        <tr @click="toggleDetails(tool.id)">
                            <td>{{ tool.name }}</td>
                            <td>{{ formatEntries(tool.inputs) }}</td>
                            <td>{{ formatEntries(tool.outputs) }}</td>
                            <td><router-link :to="'/tools/' + tool.id">View</router-link></td>
                        </tr>
                        <tr v-if="tool.showDetails" :key="'details-' + tool.id">
                            <td colspan="4">{{ tool.description }}</td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
    </div>
</template>
  
<script>
import GlobalState from '@/globalState.js';
export default {
    data() {
        return {
            tools: GlobalState.state.tools
        };
    },
    methods: {
        toggleDetails(id) {
            const tool = this.tools.find(t => t.id === id);
            if (tool) tool.showDetails = !tool.showDetails;
        },
        formatEntries(entries) {
            return Object.entries(entries).map(([key, type]) => `${key} (${type})`).join(', ');
        }
    }
}
</script>
  
<style scoped>
.tools-page {
    padding: 20px;
    width: 80%;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 1;
}

.tools-container {
    width: 100%;
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    padding: 10px 20px;
    border-bottom: 1px solid #e0e0e0;
}
td {
    cursor: pointer;
}
td:last-child {
    text-align: right;
    border: none;
    width: 1%;
    white-space: nowrap;
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
    background-color: #3498db;
    padding: 10px 20px;
    border-radius: 5px;
    color: white;
    text-decoration: none;
    transition: background-color 0.3s;
}

.create-btn:hover {
    background-color: #2980b9;
}
</style>