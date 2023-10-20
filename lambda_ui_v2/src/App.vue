<template>
    <div id="app" :class="{ 'landing-page': $route.name === 'landingpage' }">
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
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
  margin: 0;
  padding: 0;
}
#app.landing-page {
    background-color: #f5f5f5;
}
</style>