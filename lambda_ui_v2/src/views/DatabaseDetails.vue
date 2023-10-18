<template>
    <div class="database-detail">
        <template v-if="database">
                <div class="card">
                    <div class="header-container">
                    <h1>{{ database.name }}</h1>
                    <button class="delete-button" @click="deleteDatabase">Delete</button>
                </div>
                <p class="description">{{ database.description }}</p>

                <section class="columns">
                    <h2>Columns</h2>
                    <div v-for="(details, columnName) in database.columns" :key="columnName" class="column">
                        <label>{{ columnName }}</label>
                        <span class="type">{{ details.type }}</span>
                        <div v-if="details.constraints && details.constraints.length" class="constraints">
                            Constraints: {{ details.constraints.join(', ') }}
                        </div>
                    </div>
                </section>
            </div>
        </template>
        <template v-else>
            <div class="error">
                Table not found.
            </div>
        </template>
    </div>
</template>

<script>
import GlobalState from '@/globalState.js';
import axios from 'axios';
export default {
    data() {
        return {
            database: null
        };
    },
    methods: { // right now we have a temporary 1-1 relationship for tables and dbs. we just show tables for now.
        fetchDatabaseDetails() {
            const foundDatabase = GlobalState.state.databases.find(db => db.id === parseInt(this.$route.params.id));

            if (foundDatabase) {
                this.database = foundDatabase;
            } else {
                this.setNotFound();
            }
        },
        setNotFound() {
            this.database = {
                name: 'not found',
                description: 'not found',
                columns: { "not found": "not found" },
            };
        },
        async deleteDatabase() {
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': 'Bearer YOUR_TOKEN_HERE'  // if you have authentication token
                }
            };
            try {
                let response = await axios.delete(process.env.VUE_APP_BACKEND_URL + '/delete_database', { data: { id: this.database.id }, headers: config.headers });
                console.log(response)
                if (response.status === 200) {
                    console.log("Database deleted successfully!");
                    await GlobalState.fetchDatabases();
                    await GlobalState.fetchTools();
                    this.$router.push('/databases');

                } else {
                    console.error("Failed to delete the database.");
                }
            } catch (error) {
                console.error("Error deleting database:", error);
            }
        }
    },
    watch: {
        '$route'(to, from) {
            if (to.params.id !== from.params.id) {
                this.fetchDatabaseDetails();
            }
        }
    },
    mounted() {
        this.fetchDatabaseDetails();
    }
}
</script>

<style scoped>
.database-detail {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 50px 0;
}

.card {
    width: 60%;
    padding: 30px;
    background-color: #fff;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}

.columns h2 {
    border-bottom: 2px solid #eee;
    margin-bottom: 20px;
}

.column {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 15px;
    font-size: 1rem;
}

.type,
.constraints {
    background-color: #f4f4f4;
    padding: 4px 8px;
    border-radius: 3px;
}
.error {
    color: red;
    font-size: 1.2em;
    text-align: center;
    margin-top: 2em;
}
.header-container {
    position: relative;
}
.delete-button {
    background-color: red;
    color: white;
    border: none;
    padding: 10px 20px;
    margin-top: 10px;
    cursor: pointer;
    transition: 0.3s;
    position: absolute;
    top: 0;
    right: 0;
}

.delete-button:hover {
    background-color: darkred;
}
</style>