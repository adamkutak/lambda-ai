<template>
    <div class="databases-page">
        <div class="header">
            <h1>Databases</h1>
            <router-link to="/newdatabase" class="create-btn">Create New</router-link>
        </div>
        <div class="databases-container">
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Columns</th>
                        <th>Types</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="database in databases" :key="database.id">
                        <tr @click="toggleDetails(database.id)">
                            <td>{{ database.name }}</td>
                            <td>{{ Object.keys(database.columns).join(', ') }}</td>
                            <td>{{ Object.values(database.columns).map(col => col.type).join(', ') }}</td>
                            <td><router-link :to="'/databases/' + database.id">View</router-link></td>
                        </tr>
                        <tr v-if="database.showDetails" :key="'details-' + database.id" class="description-row">
                            <td colspan="4">{{ database.description }}</td>
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
            databases: GlobalState.state.databases
        };
    },
    methods: {
        toggleDetails(id) {
            const database = this.databases.find(db => db.id === id);
            if (database) database.showDetails = !database.showDetails;
        }
    }
}
</script>

<style scoped>
.databases-page {
    padding: 20px;
    width: 80%;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
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


.databases-container {
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

.description-row {
    text-align: right;
}
</style>
