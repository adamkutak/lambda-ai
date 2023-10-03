<template>
    <div class="tool-detail">
        <!-- Display only when not loading -->
        <template v-if="!loading">
            <div class="card">
                <h1>{{ tool.name }}</h1>
                <p class="description">{{ tool.description }}</p>

                <section class="parameters">
                    <h2>Inputs</h2>
                    <div v-for="(type, key) in tool.inputs" :key="key" class="parameter">
                        <label :for="'input-' + key">{{ key }}</label>
                        <input :id="'input-' + key" v-model="inputValues[key]" :placeholder="type" />
                    </div>

                    <h2>Outputs</h2>
                    <div v-for="(type, key) in tool.outputs" :key="key" class="parameter">
                        <label>{{ key }}</label>
                        <input readonly :value="outputValues[key]" :placeholder="type" />
                    </div>
                </section>

                <button @click="runTool">Run</button>
            </div>
        </template>

        <!-- Display a loader or some message while fetching the data -->
        <div v-if="loading" class="loading">
            Loading tool details...
        </div>
    </div>
</template>
  
<script>
import axios from 'axios'; // Assuming you are using axios to make API calls

export default {
    data() {
        return {
            loading: true,
            tool: {
                name: '',
                description: '',
                inputs: {},
                outputs: {}
            },
            inputValues: {},
            outputValues: {}
        };
    },
    methods: {
        async fetchToolDetails() {
            try {
                let response = await axios.get(`YOUR_API_ENDPOINT/tools/${this.$route.params.id}`);

                if (response.data) {
                    this.tool = response.data;
                } else {
                    this.tool = {
                        name: 'not found',
                        description: 'not found',
                        inputs: { "not found": "not found" },
                        outputs: { "not found": "not found" }
                    };
                }
            } catch (error) {
                console.error("Error fetching tool details:", error);
                this.tool = {
                    name: 'not found',
                    description: 'not found',
                    inputs: { "not found": "not found" },
                    outputs: { "not found": "not found" }
                };
            } finally {
                this.loading = false;
            }
        },
        async runTool() {
            try {
                let response = await axios.post('YOUR_API_ENDPOINT/run-tool', this.inputValues);

                if (response.data) {
                    this.outputValues = response.data;
                } else {
                    console.error("No data received from the API.");
                    this.outputValues = {
                        // ... default error values if necessary
                    };
                }
            } catch (error) {
                console.error("Error running tool:", error);
                this.outputValues = {
                    // ... default error values if necessary
                };
            }
        }
    },
    created() {
        this.fetchToolDetails();
    }
}
</script>

  
<style scoped>
.tool-detail {
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

.description {
    margin-top: 20px;
    margin-bottom: 30px;
    font-style: italic;
    color: #777;
}

.parameters h2 {
    border-bottom: 2px solid #eee;
    margin-bottom: 20px;
}

.parameter {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 15px;
}

input {
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
    transition: border 0.3s;
}

input:focus {
    border: 1px solid #3498db;
    outline: none;
}

button {
    margin-top: 20px;
    padding: 10px 25px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}

button:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
}

.loading {
    padding: 15px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
}
</style>