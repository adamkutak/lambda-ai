<template>
  <div class="landing-page">
    <div class="navbar">
      <div class="navbar-brand">TextTool.</div>
      <div class="navbar-actions">
        <button class="login-btn" @click="redirectToLogin">Login</button>
        <button class="register-btn" @click="redirectToRegister">Register</button>
      </div>
    </div>

    <div class="content">
      <h1>Create and Share Tools Instantly</h1>
      <!-- <p>Use them in TextTool, Excel, Zapier, or Anywhere Else.</p> -->
      <p>TextTool can build any Tool instantly from a description</p>
      <button class="learn-more-btn" @click="redirectToRegister">Try It Now</button>
      <p></p>
      <div class="screenshot-section">
        <img class="screenshot-image" src="@/assets/tool_screen.png" alt="screenshot 1">
      </div>
      <p></p>

      <h1>Add Database-quality Tables</h1>
      <p>Create simple backends using Tools + Tables</p>
      <p></p>

      <div class="screenshot-section">
        <img class="screenshot-image" src="@/assets/database_screen.png" alt="screenshot 2">
      </div>

      <h1>Build any Tool</h1>
      <p>
        Use tools in TextTool, Excel, Zapier, or as APIs <br>
        Go beyond simple integration automations and drag and drop components.<br>
        TextTool can build you complete production-grade APIs with simple descriptions<br>
        Integrate external APIs for more functionality (Coming soon)<br>
        Collaborate in your team workspace (Coming soon)<br>
      </p>
      <p></p>
      <p></p>
    </div>

    <div class="footer">
      <!-- Add footer content here -->
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
export default {
  name: 'LandingPage',
  methods: {
    async redirectToLogin() {
      const config = {
        headers: {
          'Content-Type': 'application/json',
        }
      };
      try {
        const response = await axios.post(process.env.VUE_APP_BACKEND_URL + '/authenticate', config);
        if (response.status == 200) {
          this.$router.push('/tools');
        } else {
          this.$router.push('/login');
        }
      } catch (error) {
        console.error('session_id not authenticated');
        this.$router.push('/login');
      }
    },
    redirectToRegister() {
      this.$router.push('/register');
    }
  }
};
</script>
  
  
<style scoped>
.landing-page {
  font-family: 'Roboto', sans-serif;
  padding: 50px;
  min-height: 100vh;
  height: 100%;
  margin: 0;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-size: 30px;
  font-weight: bold;
}

.navbar-actions {
  display: flex;
  gap: 10px;
}

button {
  border: none;
  padding: 10px 20px;
  /* Increased padding */
  font-size: 16px;
  /* Increased font size */
  border-radius: 4px;
  /* Optionally, adjust border-radius if you want */
  cursor: pointer;
}

.login-btn {
  background-color: #9e9e9e;
  color: #ffffff;
}

.register-btn {
  background-color: #3400db;
  color: #ffffff;
}

.content {
  margin-top: 100px;
  text-align: center;
}

h1 {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 20px;
}

p {
  font-size: 18px;
  margin-bottom: 30px;
}

.screenshot-section {
  display: flex;
  flex-direction: column;
  /* This will stack the images vertically */
  gap: 20px;
  align-items: center;
  /* This centers the images horizontally */
  margin-bottom: 50px;
}

.screenshot-image {
  width: 80%;
  /* This reduces the image width to 30% */
  /* No need to set the height as it will adjust automatically to maintain the aspect ratio */
}

.learn-more-btn {
  background-color: #3400db;
  color: #ffffff;
}
</style>
  