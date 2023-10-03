<template>
    <div class="database-detail">
        <!-- Display only when not loading -->
        <template v-if="!loading">
            <div class="card">
                <h1>{{ database.name }}</h1>

                <section class="columns">
                    <h2>Columns</h2>
                    <div v-for="(details, columnName) in database.columns" :key="columnName" class="column">
                        <label>{{ columnName }}</label>
                        <span class="type">{{ details.type }}</span>
                        <span v-if="details.constraints" class="constraints">{{ details.constraints }}</span>
                    </div>
                </section>
            </div>
        </template>

        <!-- Display a loader or some message while fetching the data -->
        <div v-if="loading" class="loading">
            Loading database details...
        </div>
    </div>
</template>

<script>
import axios from 'axios'; // Assuming you are using axios to make API calls

export default {
    data() {
        return {
            loading: true,
            database: {
                name: '',
                columns: {}
            }
        };
    },
    methods: {
        async fetchDatabaseDetails() {
            try {
                let response = await axios.get(`YOUR_API_ENDPOINT/databases/${this.$route.params.id}`);

                if (response.data) {
                    this.database = response.data;
                } else {
                    this.database = {
                        name: 'not found',
                        columns: { "not found": { type: "unknown", constraints: "none" } }
                    };
                }
            } catch (error) {
                console.error("Error fetching database details:", error);
                this.database = {
                    name: 'not found',
                    columns: { "not found": { type: "unknown", constraints: "none" } }
                };
            } finally {
                this.loading = false;
            }
        },
    },
    created() {
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

.loading {
    padding: 15px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
}
</style>