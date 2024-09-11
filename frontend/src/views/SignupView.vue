<!-- eslint-disable prettier/prettier -->
<template>
  <div class="form-container">
    <div class="SignUp">
      <div class="SHead">
        <h2>Register</h2>
      </div>
      <div class="SBody">
        <div class="SBody-left">
          <form @submit.prevent="registerUser">
            <div>
              <input
                type="text"
                id="username"
                placeholder="Username"
                v-model="username"
                @blur="validateUsername"
                required
              />
              <span v-if="errors.username" class="error">{{ errors.username }}</span>
            </div>
            <div>
              <input
                type="email"
                id="email"
                placeholder="Email"
                v-model="email"
                @blur="validateEmail"
                required
              />
              <span v-if="errors.email" class="error">{{ errors.email }}</span>
            </div>
            <div>
              <input
                type="password"
                id="password1"
                placeholder="Password"
                v-model="password1"
                @blur="validatePassword1"
                required
              />
              <span v-if="errors.password1" class="error">{{ errors.password1 }}</span>
            </div>
            <div>
              <input
                type="password"
                id="password2"
                placeholder="Confirm Password"
                v-model="password2"
                @blur="validatePassword2"
                required
              />
              <span v-if="errors.password2" class="error">{{ errors.password2 }}</span>
            </div>
            <div>
              <button type="submit">Register</button>
            </div>
            <div>
              <router-link to="/login" class="navbar-item">
                <button class="btn btn-SignUp">Login</button>
              </router-link>
            </div>
          </form>
        </div>
        <div class="SBody-right">
          <div>
            <input
              type="file"
              id="image"
              @change="onCoverProfile"
              class="fileValue"
              required
            />
            <label for="image" class="custom-file-upload">Profile | {{ imageName }}</label>
          </div>
          <div>
            <div class="imageView1">
              <p class="name1">Profile Image</p>
              <img v-if="imageUrl" :src="imageUrl" alt="Profile Image Preview" class="signup-image-preview" />
            </div>
          </div>
        </div>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      password1: "",
      password2: "",
      image: null,
      message: "",
      imageUrl: null,
      imageName: "",
      errors: {}, // To store validation error messages
    };
  },
  methods: {
    onCoverProfile(event) {
      this.image = event.target.files[0];
      this.imageUrl = URL.createObjectURL(this.image);
      this.imageName = this.image.name;
    },
    validateUsername() {
      if (!this.username) {
        this.errors.username = "Username is required.";
      } else {
        this.errors.username = null;
      }
    },
    validateEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.email) {
        this.errors.email = "Email is required.";
      } else if (!emailPattern.test(this.email)) {
        this.errors.email = "Invalid email format.";
      } else {
        this.errors.email = null;
      }
    },
    validatePassword1() {
      if (!this.password1) {
        this.errors.password1 = "Password is required.";
      } else if (this.password1.length < 8) {
        this.errors.password1 = "Password must be at least 8 characters long.";
      } else {
        this.errors.password1 = null;
      }
    },
    validatePassword2() {
      if (!this.password2) {
        this.errors.password2 = "Please confirm your password.";
      } else if (this.password1 !== this.password2) {
        this.errors.password2 = "Passwords do not match.";
      } else {
        this.errors.password2 = null;
      }
    },
    registerUser() {
      // Run validations before submitting
      this.validateUsername();
      this.validateEmail();
      this.validatePassword1();
      this.validatePassword2();

      // If any errors exist, do not proceed with form submission
      if (Object.values(this.errors).some((error) => error)) {
        return;
      }

      let formData = new FormData();
      formData.append("username", this.username);
      formData.append("email", this.email);
      formData.append("password1", this.password1);
      formData.append("password2", this.password2);
      formData.append("image", this.image);

      axios
        .post(`/signup`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.message = response.data.message;
          this.email = "";
          this.password1 = "";
          this.username = "";
          this.image = null;
          this.password2 = "";
          this.imageUrl = null;
          this.$router.push("/login");
        })
        .catch((error) => {
          if (error.response && error.response.data) {
            this.message = error.response.data.message;
          } else {
            this.message = "An error occurred.";
          }
        });
    },
  },
};
</script>
<!-- eslint-disable prettier/prettier -->

<style scoped>
.form-container {
  height: 100vh;
  background-image: url("https://wallpaperaccess.com/full/84303.jpg");
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: moveBackground 45s linear infinite;
  /* Adding animation */
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

h3 {
  font-size: 40px;
  color: white;
  font-weight: bold;
  font-family: Inter, sans-serif;
}

.SignUp {
  width: 600px;
  height:max-content;
  margin: 0 auto;
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
  color: #ffffff;
  /* White text color for readability */
}

.SBody,
.SHead {
  text-align: center;
  padding: 10px;
  width: 100%;
}
.SBody{
  display: flex;
  flex-direction: row;
}
.SBody-left{
  width:100%;
}
.SBody-right{
  width:100%;
}
.SignUp h3 {
  text-align: center;
}

.SignUp form {
  display: flex;
  flex-direction: column;
}
.fileValue{
  overflow: hidden;
}
.SignUp label,
.SignUp input,
.SignUp button {
  text-align: center;
  margin-bottom: 15px;
  padding: 10px;
  width: 90%;
  border-radius: 20px;
  overflow: hidden;
}

.SignUp button {
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
.imageView1{
    width: 240px;
    height: 200px;
    margin: 20px;
    overflow: hidden;
    border: 3px solid #C8ACD6;
    border-radius: 20px;
}
.signup-image-preview{
  width: 240px;
    height: 200px;
}
.SignUp button:hover {
  color: rgb(255, 255, 255);
  background-color: #695bb7;
}

.SignUp p {
  color: rgb(255, 255, 255);
}
.custom-file-upload{
  overflow: hidden;
}

.SignUp input {
  margin: 10px 0;
  font-size: 18px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff; /* White text color */
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}
input[type="file"] {
    display: none;
}

.SignUp input::placeholder {
  color: rgba(255, 255, 255, 0.7); /* Placeholder color */
}
.error {
  color: red;
  font-size: 0.9em;
  margin-top: 5px;
}


@media (max-width: 768px) {
  .SBody{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.form-container {
  height: 120vh;
}
}
</style>
