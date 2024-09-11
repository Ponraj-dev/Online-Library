<!-- eslint-disable prettier/prettier -->
<template>
    <div class="dashboard">
        <div class="content">
            <div class="header2">
                <div class="title">
                    <p>Discover</p>
                    <router-link to="/search" class="search">
                        <i class="fa-solid fa-magnifying-glass"></i>Search
                    </router-link>

                </div>
                <div v-if="!isAdmin" class="profileicon">
                    <router-link to="/profile" class="profileCard"><img :src="getUserImage(user.profile_image)" alt="Profile Image" class="profile-page-image" />
                    <p class="profileName">{{
                        user.username
                    }}</p></router-link>
                </div>
                <div v-if="isAdmin" class="profileicon">
                    <img src="../assets/download.jpg" alt="Profile Image" class="profile-page-image" />
                    <router-link to="/adminDashboard" class="profileName">Admin</router-link>
                </div>
                <!-- <div class="search-bar">
                    <select class="categories">
                        <option>All Categories</option>
                    </select>
                    <input type="text" placeholder="Find the book you like..." />
                    <button>Search</button>
                </div> -->
            </div>
            <div class="book-recommendation">
                <p>Book Recommendation</p>
                <div class="book-list">
                    <!-- Add book items here -->
                    <Ebooks @book-selected="showSelectedBook" />
                </div>
            </div>
            <div class="book-category">
                <p>Book Category</p>
                <div class="category-list">
                    <Section />
                </div>
            </div>
        </div>
        <div class="selected-book" v-if="selectedBookId">
            <SelectedBook :bookId="selectedBookId.toString()" @close="selectedBookId = null" />
        </div>
        <div class="selected-book" v-if="!selectedBookId">
            <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel" data-bs-interval="3000">
                <div class="carousel-indicators">
                    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
                    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
                    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="3" aria-label="Slide 4"></button>
                    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="4" aria-label="Slide 5"></button>
                </div>
                <div class="carousel-inner">
                    <div class="carousel-item active">
                        <img src="../assets/ad1.jpg" alt="Ad 1">
                    </div>
                    <div class="carousel-item">
                        <img src="../assets/ad2.jpg" alt="Ad 2">
                    </div>
                    <div class="carousel-item">
                        <img src="../assets/ad3.jpg" alt="Ad 3">
                    </div>
                    <div class="carousel-item">
                        <img src="../assets/ad4.jpg" alt="Ad 3">
                    </div>
                    <div class="carousel-item">
                        <img src="../assets/ad5.jpg" alt="Ad 3">
                    </div>
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>

    </div>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
import SelectedBook from "@/components/selectedBook.vue";
import Ebooks from "../components/Ebooks.vue";
import Section from "@/components/section.vue";
import axios from "axios";

export default {
    data() {
        return {
            isAdmin: localStorage.getItem("userRole") == "admin",
            user: {
                profile_image: "",
            },
            selectedBookId: null,
        };
    },
    components: {
        Ebooks,
        SelectedBook,
        Section,
    },
    mounted() {
        // Fetch user data when the component is mounted
        this.fetchUsers();
    },
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            // Optionally provide a placeholder image or handle empty image case
            return "https://via.placeholder.com/150"; // Example: return '/default-profile-image.jpg';
        },
        fetchUsers() {
            let token = localStorage.getItem("accessToken");

            axios
                .get("/dashboard", {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        Authorization: `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    // Log the response data to verify the structure
                    console.log(response.data);
                    // Assign the user data correctly
                    this.user = response.data.user;
                })
                .catch((error) => {
                    console.error("There was an error fetching the users!", error);
                });
        },
        showSelectedBook(bookId) {
            this.selectedBookId = bookId;
        },
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
.dashboard {
    padding-top: 20px;
    display: flex;
    flex-direction: row;
    height: 100%;
    width: 100%;
    background-image: radial-gradient(circle, #433d8b, #17153b);
}

.content {
    width: 100%;
    flex: 0 0 80%;
}

.selected-book {
    margin-top: 5%;
    padding-top: 20px;
    display: flex;
    align-items: center;
    flex: 0 0 20%;
}
.carousel-inner {
    width: 100%;
    height: 100%;
}

.carousel-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}

.selected-book .carousel {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
}

.header2 {
    display: flex;
    flex-direction: column;
}

.title {
    display: flex;
    padding: 10px;
    font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
    font-size: 30px;
    font-weight: bold;
    align-self: start;
    flex-direction: row;
}

.profileicon {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color:#C8ACD6;
}
.profileicon:hover{
    background-color: #b789ce;
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}
.profileCard{
    display: flex;
    justify-content:center;
    text-decoration: none;
    border-radius: 15px;
}

.profileName {
    font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande",
        "Lucida Sans Unicode", Geneva, Verdana, sans-serif;
    text-decoration: none;
    color: rgb(60, 60, 60);
}

.profile-page-image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.search {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    border-radius: 25px;
    background-color: #f0f0f0;
    text-decoration: none;
    color: #333;
    font-size: 16px;
    transition: all 0.3s ease;
    margin: 10px;
    font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande",
        "Lucida Sans Unicode", Geneva, Verdana, sans-serif;
    text-decoration: none;
}

.search:hover {
    background-color: #e0e0e0;
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

.search i {
    margin-right: 10px;
    font-size: 18px;
    color: #666;
    transition: color 0.3s ease;
}

.search:hover i {
    color: #333;
}

.search:active {
    background-color: #d6d6d6;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transform: translateY(0);
}

.search:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(100, 150, 250, 0.5);
}

.search:visited {
    color: #333;
}

.search-bar {
    padding: 10px;
    border-radius: 10px;
    display: flex;
    justify-content: start;
    max-width: fit-content;
    background-color: #ffffff;
    border: 1px solid #ccc;
}

.categories {
    padding: 5px;
    margin-right: 10px;
    border: 0px solid #ccc;
    border-radius: 5px;
}

.search-bar input {
    padding: 5px;
    margin-right: 10px;
    border: 0px solid #ccc;
    border-radius: 5px;
}

.search-bar button {
    padding: 5px 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.book-recommendation,
.book-category {
    padding: 10px;
    margin: 10px;
    font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
    font-size: 20px;
    font-weight: bold;
    color: #707070f2 !important;
    align-self: start;
    background-color: #110b2d96;
    border-radius: 20px;
}

.book-list,
.category-list {
    display: flex;
    overflow-x: auto;
}

.book-list>div,
.category-list>div {
    margin-right: 10px;
    flex: 0 0 auto;
}

.book-list img,
.category-list img {
    width: 150px;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.book-list h4,
.category-list h4 {
    margin-top: 10px;
}
@media (min-width: 769px) {
    .profileicon {
    position: absolute;
    right: 10px;
    display: flex;
    padding: 10px;
    border-radius: 85px;
    background-color: #C8ACD6;
    font-size: 20px;
}
.profileicon:hover{
    background-color: #c292dad6;
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

}
@media (max-width: 768px) {
    .profileName{
        text-decoration-style: none;
        padding: 10px;
}
.profileicon {
    position: absolute;
    right: 10px;
    display: flex;
    padding: 10px;
    border-radius: 85px;
    background-color: #e3e0e0d6;
    font-size: 20px;
}
.profile-page-image {
    margin-right: 0px;
}
.dashboard{
    display:block;
    height: 170%;
}
.selected-book {
    padding-top: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.selected-book .carousel {
    width: 40%;
    height: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
}
}
@media (max-width: 417px) {
    .profileicon {
    display: flex;
    align-content: center;
    padding: 10px;
    border-radius: 15px;
    background-color: #e3e0e025;
    font-size: 15px;
    }
    .search {
    display: none;
}
.selected-book {
    display: none;
}
    .profileCard{
        display: flex;
        flex-direction:column;
        text-decoration-style: none;
        color: blue;
}}
</style>
