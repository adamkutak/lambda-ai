<template>
  <div class="register-page">
    <div class="register-card">
      <h1 class="app-title">TextTool.</h1>
      <h2>Register</h2>
      <router-link to="/login" class="register-link">Already have an account? Login here</router-link>

      <div class="name-container">
        <input v-model="first_name" type="text" placeholder="First Name" class="first-name" />
        <input v-model="last_name" type="text" placeholder="Last Name" class="last-name" />
      </div>
      <input v-model="email" type="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />
      <input v-model="retyped_password" type="password" placeholder="Retype Password" />
      <p :class="{ 'error-message': true, 'invisible': !passwordMismatch }">Passwords don't match</p>
      <button @click="submitRegister" class="register-btn">Register</button>
      <router-link to="/" class="home-link">Back to Home</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import GlobalState from '@/globalState.js';
export default {
  data() {
    return {
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      retyped_password: ''
    }
  },
  computed: {
    passwordMismatch() {
      return this.password && this.retyped_password && this.password !== this.retyped_password;
    }
  },
  methods: {
    async submitRegister() {
      if (this.password !== this.retyped_password) {
        alert('Passwords do not match.');
        return;
      }

      const config = {
        headers: {
          'Content-Type': 'application/json',
        }
      };
      const register_data = {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        password: this.password,
      }
      try {
        const response = await axios.post(process.env.VUE_APP_BACKEND_URL + '/register', register_data, config);
        console.log(response)
        if (response.status == 200) {
          await GlobalState.init()
          this.$router.push('/tools');
        } else {
          // Handle failed register, e.g., showing an error message
          alert('Registration failed. Please check your credentials and try again.');
        }
      } catch (error) {
        console.error('An error occurred while trying to register:', error);
        alert('An error occurred. Try again.');
      }
    }
  }
}
</script>
<style scoped>
/* Using Roboto font from the landing page for consistency */
.register-page {
  font-family: 'Roboto', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
  /* A light background for contrast with the card */
}

.name-container {
  display: flex;
  gap: 10px;
  /* Adjust this value based on your liking for the space between the two name input fields */
}

.first-name,
.last-name {
  flex: 1;
  /* Makes sure both input fields take equal width */
  box-sizing: border-box;
  /* Ensures padding is included in width calculations */
  width: calc(50% - 5px);
  /* Accounts for half the gap */
}

.register-card {
  width: 320px;
  /* Width of the card */
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  /* A slight shadow for the card effect */
  border-radius: 5px;
  background-color: #fff;
  /* White background for the card */
  display: flex;
  /* Using flexbox to align items */
  flex-direction: column;
  /* Stack items vertically */
  gap: 15px;
  /* Gap between the items */
}

.register-card h2 {
  margin-bottom: 1px;
  /* Adjust this value to your liking */
}

.app-title {
  font-size: 2em;
  /* Adjust based on your preference */
  margin-bottom: 20px;
  /* Adds some space below the title */
  font-weight: bold;
  color: #3400db;
  /* The same blue color as the button for consistency */
}

input[type="text"],
input[type="email"],
input[type="password"] {
  padding: 10px;
  border: none;
  border-bottom: 2px solid #9e9e9e;
  /* Light gray border at the bottom */
  border-radius: 0;
  /* Reset the border-radius */
  outline: none;
  font-size: 16px;
  transition: border-bottom-color 0.3s;
  /* Transition for the border color change on focus */
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="password"]:focus {
  border-bottom-color: #3400db;
  /* Change the border color to blue when the input is focused */
}

button.register-btn {
  align-self: center;
  background-color: #3400db;
  /* Using the same color from your styles */
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
  text-align: center;
  /* Centers the text in the link */
  text-decoration: none;
  color: #9e9e9e;
  /* Light gray color for the link, similar to the input border */
  transition: color 0.3s;

  /* Adds a smooth transition for hover effects */
  /* Optional hover effect to make the link darker when hovered */
  &:hover {
    color: #757575;
  }
}

.register-link {
  display: block;
  margin-bottom: 15px;
  /* Adds some space below the link */
  text-align: center;
  /* Centers the text in the link */
  text-decoration: none;
  color: #9e9e9e;
  /* Light gray color for the link */
  transition: color 0.3s;

  /* Adds a smooth transition for hover effects */
  /* Optional hover effect to make the link darker when hovered */
  &:hover {
    color: #757575;
  }
}

.error-message {
  color: red;
  font-size: 12px;
  margin-top: 1px;
  margin-bottom: 1px;
  height: 12px;
  /* This reserves space for one line of the error message */
  overflow: hidden;
  /* Just in case */
}

.invisible {
  visibility: hidden;
}
</style>
