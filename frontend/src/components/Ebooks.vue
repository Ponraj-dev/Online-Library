<!-- eslint-disable prettier/prettier -->
<template>
    <div class="book-row">
        <div v-if="ebooks.length" class="Ebook-column">
            <div v-for="ebook in ebooks" :key="ebook.id" class="ebook-card" @click="selectBook(ebook.id)">
                <img :src="getUserImage(ebook.profile_image)" alt="Profile Image" class="profile-image" />
                <div class="ebook-info">
                    <p class="bookname">{{ ebook.bookname }}</p>
                    <p class="authors">{{ ebook.Authors }}</p>
                </div>
            </div>
        </div>
        <div v-else>
            <p>No books found.</p>
        </div>
    </div>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from "axios";
export default {
    data() {
        return {
            ebooks: [],
        };
    },
    name: "Ebooks",
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ''; // Optionally provide a placeholder image
        },
        selectBook(bookId) {
        this.$emit('book-selected', bookId);
        },
        fetchUsers() {
            let token = localStorage.getItem('accessToken');

            axios
                .get('/ebooksDashboard',{
                headers: {
                    "Content-Type": "multipart/form-data",
                    'Authorization':`Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then((response) => {
                    this.ebooks = response.data.ebooks;
                })
                .catch((error) => {
                    console.error("There was an error fetching the users!", error);
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
.book-row {
    display: flex;
    flex-direction: column;
    align-self: start;
    padding-left: 20px;
    scroll-padding-bottom: 20px;
}

.ebook-card {
    display: flex;
    flex-direction: column;
    background-color: #efdaf9f5;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    width: 200px;
    height: 300px; /* Fixed height for the card */
    margin: 20px;
    text-align: center;
    transition: transform 0.3s ease-in-out;
}

.Ebook-column{
    display: flex;
    flex-direction: row;
}

.ebook-card:hover {
    transform: translateY(-10px);
}

.profile-image {
    width: 100%;
    height: 100%; /* Adjust the height to fit the card */
    object-fit: cover; /* Ensure the image covers the area while maintaining aspect ratio */
    overflow: hidden;
}


.ebook-info { /* Adjust the height to fit the remaining space */
    display: flex;
    flex-direction: column;
    align-items: center;
}


.bookname {
    font-size: 20px;
    font-weight: bold;
    color: #2E236C;
}

.authors {
    font-size: 14px;
    color: #2E236C;
}
a {
    color: inherit;
    text-decoration: none;
}
</style>