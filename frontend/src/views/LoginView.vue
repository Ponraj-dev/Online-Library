<template>
  <div class="loginPage">
    <div class="login">
      <div class="lHead">
        <h3>Login</h3>
      </div>
      <div class="lBody">
        <form @submit.prevent="validateForm">
          <div>
            <input
              type="text"
              v-model="username"
              placeholder="Username"
              id="username"
              required
            />
            <p v-if="errors.username" class="error">{{ errors.username }}</p>
          </div>
          <div>
            <input
              type="password"
              v-model="password"
              placeholder="Password"
              id="password"
              required
            />
            <p v-if="errors.password" class="error">{{ errors.password }}</p>
          </div>
          <div><button type="submit">Login</button></div>
          <p>or</p>
          <div>
            <router-link to="/signup" class="navbar-item">
              <button class="btn btn-signup">Sign Up</button>
            </router-link>
            <router-link to="/adminlogin" class="navbar-item">
              <button class="btn btn-signup">Admin login</button>
            </router-link>
          </div>
        </form>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errors: {},
      message: "",
    };
  },
  methods: {
    validateForm() {
      this.errors = {};

      if (!this.username) {
        this.errors.username = "Username is required";
      } else if (this.username.length < 5) {
        this.errors.username = "Username must be at least 5 characters long";
      }

      if (!this.password) {
        this.errors.password = "Password is required";
      } else if (this.password.length < 6) {
        this.errors.password = "Password must be at least 6 characters long";
      }

      if (Object.keys(this.errors).length === 0) {
        this.loginUser();
      }
    },
    async loginUser() {
      try {
        const response = await axios.post(
          `/login`,
          {
            username: this.username,
            password: this.password,
          },
          { withCredentials: true }
        );

        this.message = response.data.message;

        if (response.status === 200) {
          this.isAuthenticated = true;
          localStorage.setItem("accessToken", response.data.token);
          localStorage.setItem("userRole", "user");
          this.$router.push("/Dashboard");
          window.location.reload();
        }
      } catch (error) {
        if (error.response && error.response.data) {
          this.message = error.response.data.message;
        } else {
          this.message = "An error occurred.";
        }
      }
    },
  },
};
</script>

<style scoped>
h3 {
  font-size: 40px;
  color: white;
  font-weight: bold;
  font-family: Inter, sans-serif;
}
.login {
  width: 600px;
  max-height: 500px;
  margin: 0 auto;
  padding: 50px;
  border-radius: 15px;
  background: #ffffff1a;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  color: #ffffff; /* White text color for readability */
}
.lBody,
.lHead {
  text-align: center;
  padding: 10px;
  width: 100%;
}

.loginPage {
  height: 100vh;
  background-image: url("https://wallpaperaccess.com/full/399813.jpg");

  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: moveBackground 45s linear infinite;
}

@keyframes moveBackground {
  0% {
    background-position: center top;
  }
  50% {
    background-position: center bottom;
  }
  100% {
    background-position: center top;
  }
}

.login h3 {
  text-align: center;
}

.login form {
  display: flex;
  flex-direction: column;
}

.login label,
.login input,
.login button {
  text-align: center;
  margin-bottom: 15px;
  padding: 10px;
  width: 90%;
  border-radius: 20px;
}

.login button {
  text-align: center;
  padding: 10px;
  width: 90%;
  background-color: #2e236c;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  justify-content: center;
}

.login button:hover {
  color: rgb(255, 255, 255);
  background-color: #695bb7;
}

.login p {
  color: rgb(255, 255, 255);
}

.login input {
  margin: 10px 0;
  font-size: 18px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

.login input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}
</style>
