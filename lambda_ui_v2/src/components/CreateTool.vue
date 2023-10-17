<!-- TODO: handle posting a new tool (an indicator to say the tool is being generated) -->

<template>
    <div>
        <h2>Create a New Tool</h2>

        <form @submit.prevent="submitForm">
            <label for="toolName">Tool Name:</label>
            <input id="toolName" v-model="tool.name" type="text" required>

            <div class="inputs-outputs-container">
                <div class="input-output-list">
                    <div class="scrollable-list"> <!-- This div will be scrollable -->
                        <div class="header">
                            <h3>Inputs</h3>
                            <button type="button" @click="addInput">+</button> <!-- Moved here -->
                        </div>
                        <div v-for="(input, index) in tool.inputs" :key="'input-' + index" class="input-output-entry">
                            <input v-model="input.key" placeholder="Input Name" required>
                            <select v-model="input.value">
                                <option v-for="type in types" :key="type" :value="type">{{ type }}</option>
                            </select>
                            <button type="button" @click="removeInput(index)">Remove</button>
                        </div>
                        <div class="header">
                            <h3>Outputs</h3>
                            <button type="button" @click="addOutput">+</button> <!-- Moved here -->
                        </div>
                        <div v-for="(output, index) in tool.outputs" :key="'output-' + index" class="input-output-entry">
                            <input v-model="output.key" placeholder="Output Name" required>
                            <select v-model="output.value">
                                <option v-for="type in types" :key="type" :value="type">{{ type }}</option>
                            </select>
                            <button type="button" @click="removeOutput(index)">Remove</button>
                        </div>
                    </div>
                </div>
            </div>

            <label for="toolDescription">Description:</label>
            <textarea id="toolDescription" v-model="tool.description" required></textarea>
            <label for="databaseSelect">Attach Database:</label>
            <select id="databaseSelect" v-model="tool.selectedDatabase">
                <option value="null" disabled selected>None</option>
                <option v-for="db in databases" :key="db" :value="db">{{ db }}</option>
            </select>
            <button v-if="!loading && !generate_error" type="submit">Create Tool</button>
            <div v-else-if="loading">
                <span>Generating...</span>
                <!-- You can replace the following with your own spinner component or icon -->
                <!-- <img src="path_to_spinner.gif" alt="Loading..." />  -->
            </div>
            <div v-else-if="generate_error">
                <span style="color: red;">Error: Something went wrong</span>
            </div>
        </form>
    </div>
</template>
  
  
<script>
import axios from 'axios';
import GlobalState from '@/globalState.js';
export default {
    props: {
        testCases: {
            type: Array,
            default: () => []
        }
    },
    data() {
        return {
            loading: false,
            generate_error: false,
            tool: {
                name: '',
                inputs: [{ key: '', value: 'str' }],
                outputs: [{ key: '', value: 'str' }],
                description: '',
                selectedDatabase: null,
            },
            types: ['str', 'int', 'float', 'bool'],
            databases: []
        };
    },
    methods: {
        addInput() {
            this.tool.inputs.push({ key: '', value: 'str' });
        },
        removeInput(index) {
            this.tool.inputs.splice(index, 1);
        },
        addOutput() {
            this.tool.outputs.push({ key: '', value: 'str' });
        },
        removeOutput(index) {
            this.tool.outputs.splice(index, 1);
        },
        submitForm() {
            this.loading = true;
            this.generate_error = false;

            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': 'Bearer YOUR_TOKEN_HERE'  // if you have authentication token
                }
            };

            // Convert inputs and outputs list to dictionary
            // it would be great to have this be the original form of the data, instead of having to convert it.
            const inputsDict = this.tool.inputs.reduce((acc, curr) => {
                acc[curr.key] = curr.value;
                return acc;
            }, {});

            const outputsDict = this.tool.outputs.reduce((acc, curr) => {
                acc[curr.key] = curr.value;
                return acc;
            }, {});

            // Adjust the testCases to match the Pydantic model
            console.log(this.testCases)
            const formattedTestCases = this.testCases.map(tc => ({
                input: tc.inputs,
                output: tc.outputs
            }));
            console.log(formattedTestCases)


            // Prepare the final data payload
            const new_tool_data = {
                tool: {
                    ...this.tool,
                    inputs: inputsDict,
                    outputs: outputsDict
                },
                testcases: formattedTestCases
            };

            console.log(new_tool_data);

            axios.post(process.env.VUE_APP_BACKEND_URL + '/create_tool', new_tool_data, config)
                .then(response => {
                    console.log(response.data);
                    this.generate_error = false;
                    GlobalState.addTool(response.data.tool)
                    this.$router.push('/tools');  // <-- Redirect on success
                })
                .catch(error => {
                    console.error('Error posting data:', error);
                    this.generate_error = true;
                })
                .finally(() => {
                    this.loading = false;  // <-- Stop loading in any case (either success or error)
                });
        }
    }
}
</script>
  
<style scoped>
/* ... global styles ... */

form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 380px;
    min-width: 380px;
    /* Adjusted for compactness */
    margin: 0 auto;
    max-height: 90vh;
    overflow: hidden;
}

/* Tool Name */
label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
}

input[type="text"],
select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}

/* Inputs/Outputs Section */
.inputs-outputs-container {
    display: flex;
    flex-direction: column;
    /* Stack vertically for compactness */
    gap: 10px;
}

.input-output-list {
    padding: 5px 10px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
}

.scrollable-list {
    height: 250px;
    max-height: 250px;
    /* Adjust to your liking */
    overflow-y: auto;
    margin-bottom: 10px;
    /* A little space before the Add button */
}

.input-output-entry {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 10px;
}

select,
button {
    margin-left: auto;
}

/* Description */
textarea {
    width: 95%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical;
    min-height: 100px;
}

/* Buttons */
button {
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    background-color: #3498db;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #2980b9;
}

button[type="submit"] {
    display: block;
    margin: 20px auto 0;
}

.input-output-list h3 {
    margin-top: 5px;
    margin-bottom: 15px;
}

button[type="button"] {
    background-color: transparent;
    color: #a61f1f;
    font-size: 16px;
    /* Increase the font size */
    padding: 5px 10px;
    /* Add some padding for bigger touch/click area */
    border-radius: 50%;
    /* Makes the button round */
    transition: background-color 0.3s ease;
    /* Transition for hover effect */
}

button[type="button"]:hover {
    background-color: #f0f0f0;
    /* Light grey background on hover */
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
}

.header h3 {
    width: 100%;
    /* Take up the full width */
    text-align: center;
    /* Center the header text */
    margin: 0;
    /* Reset the margin for exact positioning */
}
</style>