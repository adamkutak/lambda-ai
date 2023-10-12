<template>
    <div>
        <h2>Create a New Database</h2>

        <form @submit.prevent="submitForm">
            <!-- Left Side: Database Name & Description -->
            <div class="database-info">
                <label for="dbName">Database Name:</label>
                <input id="dbName" v-model="database.name" type="text" required>

                <label for="dbDescription">Description:</label>
                <textarea id="dbDescription" v-model="database.description" required></textarea>

                <!-- Moved the Create Database button here -->
                <button v-if="!loading && !generate_error" type="submit">Create Database</button>
                <div v-else-if="loading">
                    <span>Generating...</span>
                    <!-- You can replace the following with your own spinner component or icon -->
                    <!-- <img src="path_to_spinner.gif" alt="Loading..." />  -->
                </div>
                <div v-else-if="generate_error">
                    <span style="color: red;">Error: Something went wrong</span>
                </div>
            </div>

            <!-- Right Side: Columns -->
            <div class="columns-container">
                <div class="header">
                    <h3>Columns</h3>
                    <button type="button" @click="addColumn">+</button>
                </div>

                <!-- Made this div scrollable -->
                <div class="scrollable-columns">
                    <div v-for="(column, index) in database.columns" :key="'column-' + index" class="column-entry">
                        <input v-model="column.name" placeholder="Column Name" type="text" required>

                        <select v-model="column.type" class="column-type">
                            <option v-for="type in types" :key="type" :value="type">{{ type }}</option>
                        </select>

                        <div>
                            <input type="checkbox" v-model="column.primaryKey"> Primary Key
                            <input type="checkbox" v-model="column.unique"> Unique
                        </div>

                        <!-- Changed the button text to '-' -->
                        <button type="button" @click="removeColumn(index)">-</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import GlobalState from '@/globalState.js';
export default {
    data() {
        return {
            loading: false,
            generate_error: false,
            database: {
                name: '',
                description: '',
                columns: [{ name: '', type: 'int', primaryKey: false, unique: false }]
            },
            types: ['int', 'string', 'float', 'boolean']
        };
    },
    methods: {
        addColumn() {
            this.database.columns.push({ name: '', type: 'int', primaryKey: false, unique: false });
        },
        removeColumn(index) {
            this.database.columns.splice(index, 1);
        },
        submitForm() {
            this.loading = true;
            this.generate_error = false;
            // Transforming the columns to fit the Pydantic model
            const formattedColumns = this.database.columns.map(column => ({
                name: column.name,
                type: column.type,
                primary_key: column.primaryKey,
                unique: column.unique
            }));

            // Constructing the request payload
            const requestData = {
                name: this.database.name,
                description: this.database.description,
                columns: formattedColumns
            };

            console.log(requestData);

            // Assuming you will send the requestData to your backend using Axios or some other method
            axios.post(process.env.VUE_APP_BACKEND_URL + '/create_table', requestData)
                .then(response => {
                    console.log(response.data);
                    GlobalState.addDatabase(response.data.table)
                })
                .catch(error => {
                    console.error('Error posting data:', error);
                    this.generate_error = true;
                })
                .finally(() => {
                    this.loading = false;
                });
        }

    }
}
</script>

<style scoped>
form {
    display: flex;
    gap: 20px;
    justify-content: center;
}

.database-info {
    max-width: 500px;
    flex: 1;
    padding: 10px;
}

.columns-container {
    flex: 1;
    border: 1px solid #e0e0e0;
    padding: 10px;
    border-radius: 5px;
}

label,
h3 {
    font-weight: bold;
    margin-bottom: 5px;
}

input[type="text"],
textarea,
select {
    width: 100%;
    margin-bottom: 10px;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

textarea {
    min-height: 80px;
    resize: vertical;
}

.column-entry {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 10px;
}

.column-entry div {
    display: flex;
    gap: 5px;
    align-items: flex-start;
}

button {
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    background-color: #3498db;
    color: #fff;
    cursor: pointer;
    margin-top: 10px;
}

button:hover {
    background-color: #2980b9;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.scrollable-columns {
    max-height: 74vh;
    /* Adjust based on your preference */
    overflow-y: auto;
    padding: 5px 0;
}

button[type="button"] {
    background-color: #3498db;
    border-radius: 5px;
    padding: 5px 8px;
    font-size: 16px;
}

button[type="button"]:hover {
    background-color: #2980b9;
}

.column-type {
    max-width: 100px;
    /* Adjust this value to your preference */
}
</style>
