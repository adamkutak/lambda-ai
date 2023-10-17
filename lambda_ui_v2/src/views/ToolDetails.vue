<template>
    <div class="tool-detail">
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
    </div>
</template>
  
<script>
import axios from 'axios';
import GlobalState from '@/globalState.js';

export default {
    data() {
        return {
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
        fetchToolDetails() {
            // Check in globalState.tools first
            const toolId = parseInt(this.$route.params.id, 10);
            const foundTool = GlobalState.state.tools.find(tool => tool.id === toolId);
            console.log(foundTool)

            if (foundTool) {
                this.tool = foundTool;
            } else {
                this.setNotFound();
            }
        },
        setNotFound() {
            this.tool = {
                name: 'not found',
                description: 'not found',
                inputs: { "not found": "not found" },
                outputs: { "not found": "not found" }
            };
        },
        async runTool() {
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': 'Bearer YOUR_TOKEN_HERE'  // if you have authentication token
                }
            };

            const query_data = {
                id: this.tool.id,
                inputs: this.inputValues
            }
            try {
                let response = await axios.post(process.env.VUE_APP_BACKEND_URL + '/query_tool', query_data, config);

                if (response.data) {
                    this.outputValues = response.data.output;
                    console.log(response.data.output)
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
    watch: {
        '$route'(to, from) {
            if (to.params.id !== from.params.id) {
                this.fetchToolDetails();
            }
        }
    },
    mounted() {
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

</style>