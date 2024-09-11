<!-- eslint-disable prettier/prettier  -->
<template>
    <div class="Admin">
    <div class="Adminlogin">
        <div class="Ahead"><h1>Admin Login</h1></div>
        <div class="ABody">
        <form @submit.prevent="Adminlogin">
            <div>
                <input type="text" v-model="username" id="adminId" placeholder="AdminId" required />
                <p v-if="errors.username" class="error">{{ errors.username }}</p>
            </div>
            <div>
                <input type="password" v-model="password" id="adminPwd" placeholder="Admin Password" required />
                <p v-if="errors.password" class="error">{{ errors.password }}</p>
            </div>
            <div>
                <button type="submit">Login</button>
            </div>
        </form>
        <p>or</p>
        <div>
        <router-link to="/signup" class="navbar-item">
            <button class="btn btn-signup">Sign Up</button>
        </router-link>
        <p v-if="message">{{ message }}</p>
        </div>
        </div>
    </div>
    </div>
</template>
<!-- eslint-disable prettier/prettier  -->
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
                this.errors.username = 'Username is required';
            } else if (this.username.length < 5) {
                this.errors.username = 'Username must be at least 5 characters long';
            }

            if (!this.password) {
                this.errors.password = 'Password is required';
            } else if (this.password.length < 6) {
                this.errors.password = 'Password must be at least 6 characters long';
            }

            if (Object.keys(this.errors).length === 0) {
                this.Adminlogin();
            }
        },
        async Adminlogin() {
            try {
                const response = await axios.post(
                    `/adminlogin`,
                    {
                        adminId: this.username,
                        adminPwd: this.password,
                    },
                    { withCredentials: true }
                );

                this.message = response.data.message;

                if (response.status === 200) {
                    this.isAuthenticated = true;
                    localStorage.setItem("accessToken", response.data.token);
                    console.log(response.data.token)
                    localStorage.setItem("userRole", "admin");
                    this.$router.push("/AdminDashboard");
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
    created() {
        axios.interceptors.response.use(
            (response) => {
                return response;
            },
            (error) => {
                if (error.response.status === 401) {
                    this.message = "Session expired. Please login again.";
                    this.isAuthenticated = false;
                    window.location.reload();
                }
                return Promise.reject(error);
            }
        );
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
.Admin {
    height: 100vh;
    background-image: url("https://wallpaperaccess.com/full/84303.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    display: flex;
    justify-content: center;
    align-items: center;
    animation: moveBackground 45s linear infinite; /* Adding animation */
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
.Adminlogin {
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
    color: #ffffff;
}
.error {
    color: red;
    font-size: 14px;
    margin-top: 5px;
}
.ABody,
.Ahead {
    text-align: center;
    padding: 10px;
    width: 100%;
}
.Adminlogin h1 {
    text-align: center;
}

.Adminlogin form {
    display: flex;
    flex-direction: column;
}

.Adminlogin label,
.Adminlogin input,
.Adminlogin button {
    text-align: center;
    margin-bottom: 15px;
    padding: 10px;
    width: 90%;
    border-radius: 20px;
}

.Adminlogin button {
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

.Adminlogin button:hover {
    color: rgb(255, 255, 255);
    background-color: #695bb7;
}

.Adminlogin p {
    color: red;
    text-align: center;
}

.Adminlogin input {
    margin: 10px 0;
    font-size: 18px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff; /* White text color */
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}

.Adminlogin input::placeholder {
    color: rgba(255, 255, 255, 0.7); /* Placeholder color */
}
</style>
