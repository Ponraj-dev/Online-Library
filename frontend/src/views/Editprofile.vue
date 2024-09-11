<!-- eslint-disable prettier/prettier -->
<template>
    <div class="form-container">
        <h2>Edit Profile</h2>
        <form @submit.prevent="registerUser">

            <div class="images-card">
                <img v-if="imagePreview" :src="imagePreview" alt="Profile Image" class="profile-page-image" />
                <img v-else :src="getUserImage(imageCode)" alt="Profile Image" class="profile-page-image" />
            </div>

            <label for="image" class="profileImg">Profile Image</label>
            <input type="file" id="image" @change="onImageChange" />

            <label for="username">Username</label>
            <input
                type="text"
                id="username"
                v-model="username"
                required
                @blur="validateUsername"
            />
            <p v-if="errors.username" class="error">{{ errors.username }}</p>

            <label for="email">Email</label>
            <input
                type="email"
                id="email"
                v-model="email"
                required
                @blur="validateEmail"
            />
            <p v-if="errors.email" class="error">{{ errors.email }}</p>

            <label for="password1">Password</label>
            <input
                type="password"
                id="password1"
                v-model="password1"
                required
                @blur="validatePassword"
            />
            <p v-if="errors.password1" class="error">{{ errors.password1 }}</p>

            <button type="submit" :disabled="isFormInvalid">Update Profile</button>
        </form>
        <p v-if="message">{{ message }}</p>
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
            image: null,
            imagePreview: null,
            message: "",
            errors: {},
            user: {},
            imageCode:""
        };
    },
    name: "Editprofile",
    computed: {
        isFormInvalid() {
            return Object.keys(this.errors).length > 0;
        },
    },
    methods: {
        onImageChange(event) {
            const file = event.target.files[0];
            if (file && file.type.startsWith("image/")) {
                this.image = file;
                this.imagePreview = URL.createObjectURL(file);
            } else {
                this.errors.image = "Please select a valid image file.";
            }
        },
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return "";
        },
        validateUsername() {
            if (this.username.length < 5) {
                this.errors.username = "Username must be at least 5 characters long.";
            } else {
                delete this.errors.username;
            }
        },
        validateEmail() {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(this.email)) {
                this.errors.email = "Please enter a valid email address.";
            } else {
                delete this.errors.email;
            }
        },
        validatePassword() {
            if (this.password1.length < 6) {
                this.errors.password1 = "Password must be at least 6 characters long.";
            } else {
                delete this.errors.password1;
            }
        },
        registerUser() {
            this.validateUsername();
            this.validateEmail();
            this.validatePassword();

            if (this.isFormInvalid) {
                return;
            }

            let formData = new FormData();
            formData.append("username", this.username);
            formData.append("email", this.email);
            formData.append("password1", this.password1);
            formData.append("image", this.image);
            const userId = this.$route.params.userId || '';

            axios
                .post(`/Editprofile/${userId}`, formData, {
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
                    this.imagePreview = null;
                    this.$router.push(`/profile/${userId}`);
                })
                .catch((error) => {
                    if (error.response && error.response.data) {
                        this.message = error.response.data.message;
                    } else {
                        this.message = "An error occurred.";
                    }
                });
        },
        fetchUsers() {
            let token = localStorage.getItem('accessToken');
            const userId = this.$route.params.userId || '';

            axios
                .get(`/Editprofile/${userId}`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        'Authorization':`Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    const user = response.data.user;
                    this.username = user.username;
                    this.email = user.email;
                    this.imageCode = user.profile_image
                })
                .catch((error) => {
                    console.error("There was an error fetching the user!", error);
                });
        },
    },
    created() {
        this.fetchUsers();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
.form-container {
    max-width: 500px;
    margin: auto;
    padding: 20px;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.form-container h2 {
    text-align: center;
    margin-bottom: 20px;
    font-size: 24px;
    color: #ffffff;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.form-container  label {
    font-weight: bold;
    margin-top: 10px;
    display: block;
    color: #ffffff;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.form-container ,.profileImg ,input {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    margin-bottom: 15px;
    box-sizing: border-box;
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
}

.form-container button {
    width: 100%;
    padding: 10px;
    margin-top: 20px;
    border: none;
    border-radius: 5px;
    background-color: #2e236c;
    color: white;
    font-size: 16px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease;
}

.form-container button:disabled {
    background-color: rgba(165, 214, 167, 0.3);
    cursor: not-allowed;
}

.form-container button:hover:enabled {
    background-color: rgba(76, 175, 80, 0.9);
}

.error {
    color: red;
    font-size: 14px;
    margin-top: -10px;
    margin-bottom: 10px;
}

.images-card {
    text-align: center;
    margin-bottom: 20px;
}

.profile-page-image {
    max-width: 150px;
    max-height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.6);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
</style>

