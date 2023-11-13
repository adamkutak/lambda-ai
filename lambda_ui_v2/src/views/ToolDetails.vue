<template>
    <div class="tool-detail">
        <div class="card">
            <div class="header-container">
                <h1>{{ tool.name }}</h1>
                <button class="delete-button" @click="deleteTool">Delete</button>
            </div>
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
                }
            };

            const query_data = {
                id: this.tool.id,
                inputs: this.inputValues
            }
            try {
                let response = await axios.post(process.env.VUE_APP_BACKEND_URL + '/query_tool', query_data, config);
                console.log(response.data.output);

                if (response.data.output) {
                    this.outputValues = response.data.output;
                }
            } catch (error) {
                const err_result = JSON.parse(error.response.data.error).detail[0].msg;
                console.log(err_result);
                this.populateFirstOutputWithError("error: " + err_result);
            }
        },
        populateFirstOutputWithError(errorMessage) {
            const firstKey = Object.keys(this.tool.outputs)[0];
            if (firstKey) {
                this.outputValues[firstKey] = errorMessage;
            }
        },
        async deleteTool() {
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': 'Bearer YOUR_TOKEN_HERE'  // if you have authentication token
                }
            };
            try {
                let response = await axios.delete(process.env.VUE_APP_BACKEND_URL + '/delete_tool', { data: { id: this.tool.id }, headers: config.headers });
                console.log(response)
                if (response.status === 200) {
                    console.log("Tool deleted successfully!");
                    await GlobalState.fetchTools();
                    this.$router.push('/tools');

                } else {
                    console.error("Failed to delete the tool.");
                }
            } catch (error) {
                console.error("Error deleting tool:", error);
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

.header-container {
    position: relative;
}
</style>