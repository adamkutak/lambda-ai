<template>
    <div id="app">
        <!-- You can render the router-view or other components only when appLoaded is true -->
        <router-view v-if="appLoaded"></router-view>
    </div>
</template>

<script>
import GlobalState from '@/globalState.js';

export default {
    data() {
        return {
            appLoaded: false
        };
    },
    async mounted() {
        // This will fetch the data and set the GlobalState's isLoaded to true
        await GlobalState.init();
        // Once that's done, set appLoaded to true to render the components
        this.appLoaded = true;
    }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}
</style>