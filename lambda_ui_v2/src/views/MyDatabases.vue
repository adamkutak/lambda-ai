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
                    <template v-for="row in tableRows">
                        <tr @click="toggleDetails(row.id)" v-if="!row.isDetailRow" :key="row.id">
                            <td>{{ row.name }}</td>
                            <td>{{ row.columns.join(', ') }}</td>
                            <td>{{ row.types.join(', ') }}</td>
                            <td><router-link :to="'/databases/' + row.id">View</router-link></td>
                        </tr>
                        <tr v-if="row.isDetailRow" :key="'details-' + row.id" class="description-row">
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
            databases: [
                {
                    id: 1,
                    name: "Database 1",
                    columns: ["column1", "column2"],
                    types: ["type1", "type2"],
                    description: "This is a description for Database 1.",
                    showDetails: false
                },
                {
                    id: 2,
                    name: "Database 2",
                    columns: ["column10", "column200"],
                    types: ["type10", "type200"],
                    description: "My new database has different structures.",
                    showDetails: false
                },
            ]
        };
    },
    computed: {
        tableRows() {
            const rows = [];
            this.databases.forEach(database => {
                rows.push(database);
                if (database.showDetails) {
                    rows.push({ ...database, isDetailRow: true });
                }
            });
            return rows;
        }
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
