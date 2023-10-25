<template>
  <div class="login-page">
    <div class="login-card">
      <h1 class="app-title">TextTool.</h1>
      <h2>Login</h2>
      <router-link to="/register" class="register-link">Or go here to create an Account</router-link>
      <input v-model="email" type="text" placeholder="email" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="submitLogin" class="login-btn">Login</button>
      <router-link to="/" class="home-link">Back to Home</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    async submitLogin() {
      const config = {
          headers: {
              'Content-Type': 'application/json',
          }
      };
      const login_data = {
        email: this.email,
        password: this.password
      }
      try {
        console.log(login_data)
        const response = await axios.post(process.env.VUE_APP_BACKEND_URL + '/login', login_data, config);
        console.log(response)
        if (response.status==200) {
          this.$router.push('/tools');
        } else {
          // Handle failed login, e.g., showing an error message
          alert('Login failed. Please check your credentials and try again.');
        }
      } catch (error) {
        console.error('An error occurred while trying to login:', error);
        alert('An error occurred. Try again.');
      }
    }
  }
}
</script>

<style scoped>
/* Using Roboto font from the landing page for consistency */
.login-page {
  font-family: 'Roboto', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5; /* A light background for contrast with the card */
}

.login-card {
  width: 320px; /* Width of the card */
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* A slight shadow for the card effect */
  border-radius: 5px;
  background-color: #fff; /* White background for the card */
  display: flex; /* Using flexbox to align items */
  flex-direction: column; /* Stack items vertically */
  gap: 15px; /* Gap between the items */
}
.login-card h2 {
  margin-bottom: 1px; /* Adjust this value to your liking */
}
.app-title {
  font-size: 2em; /* Adjust based on your preference */
  margin-bottom: 20px; /* Adds some space below the title */
  font-weight: bold;
  color: #3400db; /* The same blue color as the button for consistency */
}
input[type="text"], input[type="password"] {
  padding: 10px;
  border: none;
  border-bottom: 2px solid #9e9e9e; /* Light gray border at the bottom */
  border-radius: 0; /* Reset the border-radius */
  outline: none;
  font-size: 16px;
  transition: border-bottom-color 0.3s; /* Transition for the border color change on focus */
}

input[type="text"]:focus, input[type="password"]:focus {
  border-bottom-color: #3400db; /* Change the border color to blue when the input is focused */
}

button.login-btn {
  align-self: center;
  background-color: #3400db; /* Using the same color from your styles */
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}
.home-link {
  display: block;
  margin-top: 10px;
  text-align: center; /* Centers the text in the link */
  text-decoration: none;
  color: #9e9e9e; /* Light gray color for the link, similar to the input border */
  transition: color 0.3s; /* Adds a smooth transition for hover effects */

  /* Optional hover effect to make the link darker when hovered */
  &:hover {
      color: #757575;
  }
}
.register-link {
  display: block;
  margin-bottom: 15px; /* Adds some space below the link */
  text-align: center; /* Centers the text in the link */
  text-decoration: none;
  color: #9e9e9e; /* Light gray color for the link */
  transition: color 0.3s; /* Adds a smooth transition for hover effects */
  /* Optional hover effect to make the link darker when hovered */
  &:hover {
      color: #757575;
  }
}
</style>
  