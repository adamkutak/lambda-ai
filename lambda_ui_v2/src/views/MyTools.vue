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