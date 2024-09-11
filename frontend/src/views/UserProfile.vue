<!-- eslint-disable prettier/prettier -->
<template>
    <div class="user-profile-page">
        <div class="user-profile">
            <div v-if="user.username" class="profile-card">
                <div class="images-card">
                    <img :src="getUserImage(user.profile_image)" alt="Profile Image" class="profile-page-image" />
                </div>
                <div class="user-info">
                    <p>{{ user.username }}</p>
                    <p>{{ user.email }}</p>
                </div>
                <div v-if="!isAdmin">
                    <button v-if="isAuthenticated" @click="logout" class="profile-buttons">
                        <i class="fas fa-sign-out-alt"></i>
                        <span>Logout</span>
                    </button>
                    <button v-if="isAuthenticated" @click="editProfile" class="profile-buttons">
                        <i class="fas fa-edit"></i>
                        <span>edit</span>
                    </button>
                </div>
                <div v-if="isAdmin">
                    <button v-if="isAuthenticated" @click="deleteUser" class="profile-buttons">
                        <i class="fa-solid fa-user-xmark"></i>
                        <span>  delete</span>
                    </button>
                </div>
            </div>
            <div v-else>
                <p>No users found.</p>
            </div>
        </div>
        <div v-if="user.username" class="user-profile">
            <p>No.of Books have</p>
            <p class="bookCount">{{ user.book_count }}</p>
        </div>
        <div class="Ebook-column">
        <div v-for="ebook in my_books" :key="ebook.id" class="section1" >
            <img :src="getUserImage(ebook.profile_image)" alt="Profile Image" class="profile-image-book" />
            <div class="ebook-info ">
                <p class="bookname p-info">{{ ebook.bookname }}</p>
                <p class="authors">written by : {{ ebook.Authors }}</p>
                <p class="authors"> {{ ebook.description }}</p>
                <p class="authors"> {{ ebook.due_date }}</p>
                <p class="days_left"> {{ ebook.days_left }} days left</p>
            </div>

        </div>
    </div>

    </div>
</template>
<!-- eslint-disable prettier/prettier -->

<script>

import axios from "axios";
export default {
    data() {
        return {
            user: {},
            isAuthenticated: true,
            isAdmin: localStorage.getItem("userRole") == "admin",
            my_books:{},
        };
    },
    name: "profile",
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ''; // Example: return '/default-profile-image.jpg';
        },
        fetchUsers() {
            let token = localStorage.getItem('accessToken');
            const userId = this.$route.params.userId || '';

            axios
                .get(`/profile/${userId}`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.user = response.data.user;
                })
                .catch((error) => {
                    console.error("There was an error fetching the users!", error);
                });
        },
        async logout() {
            try {
                const response = await axios.post("/logout", {}, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("accessToken")}`,
                        'Content-Type': 'application/json'  // Specify content type if needed
                    },
                    withCredentials: true
                });
                if (response.status === 200) {
                    this.isAuthenticated = false;
                    this.isAdmin = false;
                    localStorage.removeItem("userRole");
                    localStorage.removeItem("accessToken");
                    this.$router.push("/login");
                }
            } catch (error) {
                this.isAuthenticated = false;
                    this.isAdmin = false;
                    localStorage.removeItem("userRole");
                    localStorage.removeItem("accessToken");
                    this.$router.push("/login");
                }
            },
        deleteUser(userId) {
            let token = localStorage.getItem('accessToken');
            axios
                .delete(`/delete_user/${userId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                })
                .then(() => {
                    this.fetchUsers();

                })
                .catch((error) => {
                    console.error("There was an error deleting the user!", error);
                });
        },
        fetchBookDetails() {
            let token = localStorage.getItem('accessToken');
            const bookId = this.$route.params.bookId || ''
            this.selectedBook = bookId

            axios
                .get(`/mybooks`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.my_books = response.data.my_books;
                })
                .catch((error) => {
                    console.error("There was an error fetching the users!", error);
                });
        },
        editProfile() {
            this.$router.push(`/editprofile/${this.user.id}`);
        },
    },
    created() {
        this.fetchUsers();
        this.fetchBookDetails();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style>
.Ebook-column {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-wrap: wrap;
}
.section1{
    display: flex;
    flex-wrap: wrap;
    width: fit-content;
    background-color: #110b2d96;
}
.user-profile {
    padding: 50px;
    margin: 30px;
    height: fit-content;
    flex-direction: column;
    align-content: center;
    background-color: #2E236C;
    border-radius: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.user-profile-page{
    display: flex;
    flex-wrap: wrap;
    background-color: #110b2d96;
}
.images-card {
    width:200px;
    margin: 10px;
    border-radius: 10%;
    object-fit: cover;
    /* Ensure the image covers the area while maintaining aspect ratio */
    overflow: hidden;
}
.days_left{
    font-size: 20px;
    color:red;
}
.profile-page-image {
    width: 100%;
    /* Adjust the height to fit the card */
    object-fit: cover;
    /* Ensure the image covers the area while maintaining aspect ratio */
    overflow: hidden;
}
.bookCount{
    font-size: 15rem;
    font-weight: 900;
    text-align: center;
    font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif
}
.p-info{
    color: rgb(255, 219, 251);
}
.user-info {
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    font-size: large;
    text-align: center;
}

.profile-buttons {
    text-decoration: none;
    padding: 5px;
    margin: 20px;
    color: #ffffff;
    background-color: rgba(0, 0, 0, 0);
    border: 2px solid rgb(255, 255, 255);
    border-radius: 10px;

}

.profile-buttons:hover {
    background-color: #1a0c76;
    transition-delay: 0.3;
    color: white;
}
</style>
