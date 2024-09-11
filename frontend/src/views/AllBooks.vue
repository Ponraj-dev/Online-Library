<!-- eslint-disable prettier/prettier -->
<template>
    <div class="book-row AllBooks">
        <h3>All Books</h3>
        <div v-if="ebooks.length" class="Ebook-column">
            <div v-for="ebook in ebooks" :key="ebook.id" class="ebook-card" @click="selectBook(ebook.id)">
                <router-link v-if="ebook.issued && ebook.status === 'Issued' || isAdmin" :to="{ name: 'EbookPage', params: { bookId: ebook.id } }">
                <img :src="getUserImage(ebook.profile_image)" alt="Profile Image" class="profile-image-AllBook" /> </router-link>
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
            isAdmin: localStorage.getItem('userRole') === 'admin',
        };
    },
    name: "AllBooks",
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
                .get('/AllBooks',{
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

h3{
    font-size: 40px;
    padding-left: 40px;
    padding-top: 20px;
    color:white;
    font-weight: bold;
    font-family: Inter, sans-serif;
}
.ebook-card {
    display: flex;
    flex-direction: column;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
     /* Fixed height for the card */
    margin: 20px;
    height: 300px;
    width:200px;
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
.ebook-card img{
    object-fit: cover;

}
.profile-image-AllBook {
    height: 300px;
    width:200px;
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