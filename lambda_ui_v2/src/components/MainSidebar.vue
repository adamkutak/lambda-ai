<template>
    <div class="sidebar">
        <router-link to="/tools">Tools</router-link>
        <router-link to="/databases">Databases</router-link>
    </div>
</template>
  
<style scoped>
.sidebar {
    width: 200px;
    height: calc(100vh - 60px);
    background-color: #2c3e50;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.sidebar a {
    color: #fff;
    /* Lighter text for better visibility on the dark background */
    text-decoration: none;
    padding: 10px;
    border-radius: 4px;
    /* Slightly rounded corners */
    transition: background-color 0.3s;
    /* Smooth transition effect */
}

.sidebar a:hover {
    background-color: #34495e;
    /* Slightly darker background on hover */
}

.sidebar a.router-link-exact-active {
    background-color: #e74c3c;
    /* Different background color for the active link */
    color: #fff;
}
</style>