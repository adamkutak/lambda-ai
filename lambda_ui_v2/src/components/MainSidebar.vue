<template>
    <div class="sidebar">
        <div class="sidebar-content">

            <div class="menu-item-wrapper">
                <router-link to="/tools" class="menu-item">
                    Tools
                </router-link>
                <span @click.stop="toggleToolsMenu" class="arrow">{{ toolsMenuVisible ? '▼' : '►' }}</span>
            </div>
            <div v-if="toolsMenuVisible" class="submenu">
                <router-link v-for="tool in tools" :key="tool.id" :to="`/tools/${tool.id}`">{{ tool.name }}</router-link>
            </div>
            <router-link to="/newtool">Create Tool</router-link>

            <div class="menu-item-wrapper">
                <router-link to="/databases" class="menu-item">
                    Databases
                </router-link>
                <span @click.stop="toggleDatabasesMenu" class="arrow">{{ databasesMenuVisible ? '▼' : '►' }}</span>
            </div>

            <div v-if="databasesMenuVisible" class="submenu">
                <router-link v-for="db in databases" :key="db.id" :to="`/databases/${db.id}`">{{ db.name }}</router-link>
            </div>
            <router-link to="/newdatabase">Create Database</router-link>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            toolsMenuVisible: false,
            databasesMenuVisible: false,
            tools: [ // Sample data
                { id: 1, name: 'Tool 1' },
                { id: 2, name: 'Tool 2' },
                // ... add as many as you'd like
            ],
            databases: [ // Sample data
                { id: 1, name: 'Database 1' },
                { id: 2, name: 'Database 2' },
                // ... add as many as you'd like
            ],
        };
    },
    methods: {
        toggleToolsMenu() {
            this.toolsMenuVisible = !this.toolsMenuVisible;
            // this.databasesMenuVisible = false; // Close other dropdowns
        },
        toggleDatabasesMenu() {
            this.databasesMenuVisible = !this.databasesMenuVisible;
            // this.toolsMenuVisible = false; // Close other dropdowns
        },
    }
}
</script>

<style scoped>
.sidebar {
    width: 240px;
    height: calc(100vh - 19px);
    background-color: #2c3e50;
    overflow-y: auto;
}

.sidebar-content {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.sidebar a,
.menu-item {
    color: #fff;
    text-decoration: none;
    padding: 10px;
    border-radius: 4px;
    transition: background-color 0.3s;
    display: flex;
    justify-content: left;
    /* Center the main content */
    align-items: center;
    position: relative;
    /* Will be used for absolute positioning of arrow */
    cursor: pointer;
    flex: 1;
    text-align: left;
}

.sidebar a:hover {
    background-color: #34495e;
}

.sidebar a.router-link-exact-active {
    background-color: #e74c3c;
}

.arrow {
    cursor: pointer;
    color: #fff;
    position: absolute;
    /* Make it absolute */
    right: 5px;
    /* 15px from the right */
    top: 50%;
    /* Center it vertically */
    transform: translateY(-50%);
    /* Fine-tune the vertical centering */
}

.submenu {
    padding-left: 40px;
    margin-top: -5px;
    /* Adjust the top margin to control vertical spacing */
}

.submenu a {
    display: block;
    margin: 3px 0;
    /* Reduced margin for less spacing between submenu items */
}

.menu-item-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    /* Necessary for absolute positioning inside it */
    cursor: pointer;
}
</style>