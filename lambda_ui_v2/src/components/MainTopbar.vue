<!-- This is a failed top bar experiment. Could be fixed some point in the future... -->
<template> 
    <div class="top-bar">
        <div></div> <!-- Empty div for left side, to center the title -->
        <div class="title">TextTool.</div>
        <button @click="logout" class="logout-btn">Log Out</button>
    </div>
</template>

<script>
export default {
    methods: {
        logout() {
            // Implement your logout logic here
            console.log("Logging out");
        }
    }
}
</script>

<style scoped>
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
    padding: 0 20px;
    background-color: #333;
    color: #fff;
}

.title {
    font-size: 24px;
    font-weight: bold;
    font-family: 'Roboto'
}

.logout-btn {
    border: none;
    background-color: transparent;
    color: #fff;
    cursor: pointer;
    transition: opacity 0.2s;

    &:hover {
        opacity: 0.8;
    }
}
</style>