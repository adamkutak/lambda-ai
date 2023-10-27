import { reactive } from 'vue';
import axios from 'axios';

const state = reactive({
    tools: [],
    databases: [],
    isLoaded: false
});

export default {
    state,

    async fetchTools() {
        const config = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        try {
            const response = await axios.get(process.env.VUE_APP_BACKEND_URL + '/get_tools', config);
            state.tools = response.data.tools;
        } catch (error) {
            console.error('Error fetching tools:', error);
        }
    },

    async fetchDatabases() {
        const config = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        try {
            const response = await axios.get(process.env.VUE_APP_BACKEND_URL + '/get_tables', config);
            state.databases = response.data.tables;
        } catch (error) {
            console.error('Error fetching databases:', error);
        }
    },

    addTool(newTool) {
        state.tools.push(newTool);
    },

    addDatabase(newDatabase) {
        state.databases.push(newDatabase);
    },


    async init() {
        await Promise.all([this.fetchTools(), this.fetchDatabases()]);
        state.isLoaded = true;
    }
};