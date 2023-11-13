<template>
    <div>
        <h2>Test Cases</h2>

        <div v-for="(testCase, index) in testCases" :key="index" class="test-case-box">
            <!-- Inputs Section -->
            <div class="test-case-section">
                <h3>Inputs</h3>
                <div v-for="input in inputs" :key="input.key" class="field">
                    <label :for="'input-' + input.key + '-' + index" class="field-label">{{ input.key }}</label>
                    <input :id="'input-' + input.key + '-' + index" v-model="testCase.inputs[input.key]" />
                </div>
            </div>

            <!-- Outputs Section -->
            <div class="test-case-section">
                <h3>Outputs</h3>
                <div v-for="output in outputs" :key="output.key" class="field">
                    <label :for="'output-' + output.key + '-' + index" class="field-label">{{ output.key }}</label>
                    <input :id="'output-' + output.key + '-' + index" v-model="testCase.outputs[output.key]" />
                </div>
            </div>
            <!-- Database Check Section -->
            <!-- Only render the inner contents if selectedDatabase is not null -->
            <div v-if="selectedDatabase">
                <!-- If testCase.showDbCheck is true, show the db-check-section -->
                <div class="db-check-section" v-if="testCase.showDbCheck">
                    <h3>Database Check</h3>
                    <div class="field">
                        <label :for="'test-row-' + index" class="field-label">Add Test Row</label>
                        <input :id="'test-row-' + index" v-model="testCase.dbTestRow" />
                    </div>
                    <div class="field">
                        <label :for="'post-test-check-' + index" class="field-label">Post-test Check</label>
                        <input :id="'post-test-check-' + index" v-model="testCase.dbPostTestCheck" />
                    </div>
                    <button @click="removeDbCheck(index)" class="remove-db-check-btn">Remove</button>
                </div>

                <!-- If testCase.showDbCheck is false, show the add-db-check-btn -->
                <button v-else @click="showDbCheck(index)" class="add-db-check-btn">+ add database check</button>

            </div>

            <button @click="removeTestCase(index)" class="remove-btn">-</button>
        </div>

        <button @click="addTestCase" class="add-btn">+</button>
    </div>
</template>

<script>
export default {
    props: ['inputs', 'outputs', 'selectedDatabase'],
    data() {
        return {
            testCases: []
        };
    },
    mounted() {
        // Fill two initial test cases with input/output keys
        for (let i = 0; i < 2; i++) {
            this.addTestCase();
        }
    },
    methods: {
        addTestCase() {
            const inputs = {};
            for (const input of this.inputs) {
                inputs[input.key] = "";
            }
            
            const outputs = {};
            for (const output of this.outputs) {
                outputs[output.key] = "";
            }
            
            this.testCases.push({
                inputs,
                outputs,
                showDbCheck: false,  // added this
                dbTestRow: "",       // added this
                dbPostTestCheck: ""  // added this
            });
        },
        removeTestCase(index) {
            this.testCases.splice(index, 1);
        },
        showDbCheck(index) {           // added this method
            this.testCases[index].showDbCheck = true;
        },
        removeDbCheck(index) {         // added this method
            this.testCases[index].showDbCheck = false;
            this.testCases[index].dbTestRow = "";
            this.testCases[index].dbPostTestCheck = "";
        }
    }
}
</script>

<style scoped>
h2 {
    margin-bottom: 10px;
}

.test-case-section h3 {
    margin-bottom: 0px;
    /* Adjust this value to your liking */
}

.test-case-box {
    display: flex;
    align-items: flex-start;
    gap: 5px;
    margin-bottom: 15px;
    position: relative;
    padding: 1px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    background-color: #f9f9f9;
    width: 60%;
    /* Increased the width */
    margin: 0 auto;
    min-width: 150px;
}

.test-case-section {
    padding: 1px;
}

.test-case-section:last-child {
    border-bottom: none;
}

.field-label {
    display: inline-block;
    width: 150px;
    /* Adjust the width as needed for the input/output names */
    text-align: right;
    margin-right: 5px;
}

.field {
    margin-bottom: 5px;
}

.remove-btn,
.add-btn {
    background-color: transparent;
    color: #333;
    /* Adjust this color if you want the +/- signs to be lighter or darker */
    border: none;
    font-size: 24px;
    /* Adjust the size if needed */
    padding: 5px;
    cursor: pointer;
    transition: color 0.3s ease;
}


.remove-btn:hover,
.add-btn:hover {
    color: #555;
}
.db-check-section {
    padding: 1px;
    border-top: 1px solid #e0e0e0;
}

.remove-db-check-btn,
.add-db-check-btn {
    margin-top: 10px;
    background-color: transparent;
    color: #333;
    border: none;
    padding: 5px;
    cursor: pointer;
    transition: color 0.3s ease;
}

.remove-db-check-btn:hover,
.add-db-check-btn:hover {
    color: #555;
}
</style>
