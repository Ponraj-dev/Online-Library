<!-- eslint-disable prettier/prettier -->
<template>
    <div class="SelectedBook">
        <div v-for="ebook in ebooks" :key="ebook.id" class="side-section1">
            <div class="ebook-info-side">
                <button class="close-button" @click="closeSelectedBook">x</button>
                <img :src="getUserImage(ebook.profile_image)" alt="Profile Image" class="profile-image-book" />
                <p class="bookname">{{ ebook.bookname }}</p>
                <p class="stars">
                    <span v-for="star in 5" :key="star" class="fa fa-star"
                        :class="{ 'checked': average_rating >= star }"></span>
                </p>
                <p class="authors"><b>Written by :</b> {{ ebook.Authors }}</p>
                <p class="genre"><b>Genre:</b> {{ formatGenres(ebook.genre) }}</p>
                <p class="authors">{{ ebook.description }}</p>

                <!-- Admin delete button -->
                <button v-if="isAdmin" @click="deleteBook(ebook.id)" class="book-button">Delete</button>

                <!-- Request button condition -->
                <button v-if="!isAdmin && ebook.status === 'Available' && !ebook.pending && ebook.book_count < 5 " @click="RequestBook(ebook.id)" class="book-button">Request</button>
                <p v-if="!isAdmin && ebook.book_count >= 5 && !ebook.issued" class="status-text-limit">You reached limits</p>
                <!-- Status messages -->
                <p v-if="!ebook.issued && !isAdmin && ebook.pending" class="status-text">Pending</p>
                <p v-if="ebook.issued && !isAdmin" class="status-text">Book Approved</p>

                <!-- Return button condition -->
                <button v-if="ebook.issued && !isAdmin && ebook.status === 'Issued'" @click="ReturnBook(ebook.id)" class="book-button">Return</button>
                <router-link v-if="ebook.issued && ebook.status === 'Issued' || isAdmin" :to="{ name: 'EbookPage', params: { bookId: ebook.id } }" class="sectionName"> <p class="sectionName">Read </p></router-link>
            </div>
        </div>
    </div>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from "axios";

export default {
    props: {
        bookId: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            ebooks: [],
            isAdmin: localStorage.getItem('userRole') === 'admin',
            average_rating: "",
        };
    },
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ''; // Optionally provide a placeholder image
        },
        formatGenres(genres) {
            return genres ? genres.join(', ') : 'No genres available';
        },
        fetchBookDetails() {
            const token = localStorage.getItem('accessToken');

            axios
                .get(`/bookspage/${this.bookId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.ebooks = response.data.ebooks;
                    this.average_rating = response.data.average_rating;
                })
                .catch((error) => {
                    console.error('There was an error fetching the book details!', error);
                });
        },
        deleteBook(bookId) {
            const token = localStorage.getItem('accessToken');
            axios
                .delete(`/deletebook/${bookId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                .then(() => {
                    this.$emit('close');
                    window.location.reload();

                })
                .catch((error) => {
                    console.error('There was an error deleting the book!', error);
                });
        },
        RequestBook(bookId) {
            const token = localStorage.getItem('accessToken');
            axios
                .post(`/requestbook/${bookId}`, {}, {
                    headers: {
                        "Content-Type": "application/json",
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then(() => {
                    this.fetchBookDetails(); // Refresh book details after requesting
                })
                .catch((error) => {
                    console.error('There was an error requesting the book!', error);
                });
        },
        ReturnBook(bookId) {
            const token = localStorage.getItem('accessToken');
            axios.post("/returnbook", { bookId }, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                withCredentials: true,
            })
            .then(() => {
                this.fetchBookDetails(); // Refresh book details after returning
            })
            .catch((error) => {
                console.error('There was an error returning the book!', error);
            });
        }, closeSelectedBook() {
            this.$emit('close');
        },
    },
    watch: {
        bookId: 'fetchBookDetails',
    },
    created() {
        this.fetchBookDetails();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style>
.side-section1 {
    display: flex;
    background-color:#181238da;
    border-radius: 22px;
}

.SelectedBook {
    height: 100%;
}
.sectionName{
    font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 20px;
    text-decoration: none;
    color:rgb(63, 63, 63);
}
.sectionName:hover{
    color:rgba(0, 255, 255, 0.719);
}
.close-button {
    position: absolute;
    right: 40px;
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    border: 2px solid rgb(255, 255, 255);
    color:white;
    border-radius: 10px;
}
.issued{
    color:rgb(96, 197, 96)
}
.profile-image-book {
    border-radius: 20px;
}

.bookname {
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 50px;
}
.ebook-info-side{
    padding: 20px;
    text-decoration: none;
}
.book-button {
    padding: 5px 15px;
    border-radius: 10px;
    border: none;
    color: rgb(0, 0, 0);
    cursor: pointer;
    background-color: rgb(192, 140, 201);
}

.book-button:hover {
    color: rgb(85, 90, 125);
    transition-delay: 0.3s;
    background-color: rgb(37, 28, 97);
}
.status-text-limit{
    color: red;
}


.checked {
    color: orange;
}

.rating-form,
.rating-display {
    margin: 20px 0;
}

.rating-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}


.stars {
    display: inline-block;
}

.fa-star {
    font-size: 20px;
    cursor: pointer;
}

</style>