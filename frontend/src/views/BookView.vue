<!-- eslint-disable prettier/prettier -->
<template>
    <div v-if="ebooks.length" class="Ebook-column">
        <div v-for="ebook in ebooks" :key="ebook.id" class="section1">
            <img :src="getUserImage(ebook.profile_image)" alt="Profile Image" class="profile-image-book" />
            <div class="ebook-info">
                <p class="bookname">{{ ebook.bookname }}</p>
                <p class="stars">
                    <span v-for="star in 5" :key="star" class="fa fa-star"
                        :class="{ 'checked': average_rating >= star }"></span>
                </p>
                <p class="authors">written by : {{ ebook.Authors }}</p>
                <p class="authors"> {{ ebook.description   }}</p>
                <p class="last-row">
                    <button v-if="isAdmin" @click="deleteBook(ebook.id)" class="book-button">Delete</button>
                    <button v-if="ebook.issued && !isAdmin && ebook.status === 'Issued'" @click="ReturnBook(ebook.id)"
                        class="book-button">Return</button>
                    <button v-if="isAdmin" @click="editBook(ebook.id)" class="book-button">Edit</button>
                    <router-link :to="{ name: 'Purchase', params: { bookId: ebook.id } }">
                        <div class="golden-btn"> $ buy </div>
                    </router-link>
                </p>
            </div>

        </div>
        <div class="section2">
            <div class="pdf-container">
                <embed :src="getBookpdf(bookpdf)" v-if="bookpdf" type="application/pdf" class="pdf-viewer" />
                <div v-else>
                    <div class="wrong_move">
                        <div>
                            <h1>Unwanted move</h1>
                        </div>
                        <div><img src="../assets/worng_move.gif" alt="profile"></div>
                        <div><button @click="goBack" class="go-back">Go Back</button></div>

                    </div>
                </div>
                <div class="pdf-overlay" @click="NotAllowed()"></div>
            </div>
        </div>
        <div class="rating-form" v-if="!isAdmin">
            <div>
                <h3>Rate this Book</h3>
                <form @submit.prevent="submitRating">
                    <div class="form-group">
                        <label>Rating:</label>
                        <div class="stars">
                            <span v-for="star in 5" :key="star" class="fa fa-star"
                                :class="{ 'checked': rating.value >= star }" @click="setRating(star)"></span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="description">Description:</label>
                        <textarea v-model="rating.description" required></textarea>
                    </div>
                    <button type="submit" class="book-button">Submit Rating</button>
                </form>
            </div>
            <div class="rating-display">
                <h3>User Ratings</h3>
                <div v-if="ratings.length">
                    <div v-for="(rate, index) in ratings" :key="index" class="rating-item">
                        <div class="rating-header">
                            <span class="user-name">{{ rate.rated_by }}</span>
                            <div class="stars">
                                <span v-for="star in 5" :key="star" class="fa fa-star"
                                    :class="{ 'checked': rate.rating_value >= star }"></span>
                            </div>
                        </div>
                        <div class="rating-description">
                            <p>{{ rate.rating_description }}</p>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <p>No ratings yet.</p>
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <p>No books found. {{ message }}</p>
    </div>



</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from "axios";

export default {
    data() {
        return {
            message: "",
            ebooks: [],
            bookpdf: '',
            isAdmin: localStorage.getItem('userRole') == "admin",
            rating: {
                value: null,
                description: ''
            },
            ratings: [],
            average_rating: "",

        };
    },
    name: "EbookPage",
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ''; // Optionally provide a placeholder image
        }, NotAllowed() {
            alert('your not allowed to print or download pdf ')
        },

        getBookpdf(base64PDF) {
            if (base64PDF) {
                return `data:application/pdf;base64,${base64PDF}`;
            }
            return ''; // Optionally provide a placeholder
        },
        getBookImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return "";
        },
        fetchUsers() {
            let token = localStorage.getItem('accessToken');
            const bookId = this.$route.params.bookId || ''
            this.selectedBook = bookId

            axios
                .get(`/bookspage/${bookId}`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.ebooks = response.data.ebooks;
                    this.bookpdf = response.data.bookpdf;
                    this.ratings = response.data.rating;
                    this.average_rating = response.data.average_rating;

                })
                .catch((error) => {
                    console.error("There was an error fetching the users!", error);
                });
        },
        deleteBook(bookId) {
            let token = localStorage.getItem('accessToken');
            axios
                .delete(`/deletebook/${bookId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        "Content-Type": "multipart/form-data",
                    },
                })
                .then(() => {
                    this.$router.push("/dashboard");

                })
                .catch((error) => {
                    console.error("There was an error deleting the user!", error);
                });
        }, ReturnBook(bookId) {
            const token = localStorage.getItem('accessToken');
            axios.post("/returnbook", { bookId }, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then(() => {
                    this.$router.push("/mybooks");
                })
                .catch((error) => {
                    console.error('There was an error returning the book!', error);
                });
        },
        editBook(BookId) {
            console.log(BookId)
            this.$router.push(`/EditBook/${BookId}`);
        },
        setRating(value) {
            this.rating.value = value;
        },
        submitRating() {
            const token = localStorage.getItem('accessToken');
            const ratingData = {
                value: this.rating.value,
                description: this.rating.description,
                ebook_id: this.selectedBook,
            };
            axios.post('/ratebook', ratingData, {
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then((response) => {
                    this.message = response.data.message;
                    alert('Rating submitted successfully!');
                    this.rating.value = 0;
                    this.rating.description = '';
                })
                .catch((error) => {
                    console.error('There was an error submitting the rating!', error);
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
.section1 {
    display: flex;
    padding: 20px;
    margin: 20px;
    background-color: #2E236C;
    border-radius: 10px;
    width: 180vh;
}

.Ebook-column {
    height: 100%;
}

.profile-image-book {
    margin-right: 20px;
}

.bookname {
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 50px;
}

.wrong_move{
    display: flex;
    flex-direction: column;
    align-content: center;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    width: 100%;
    height: 100vh;
}
.wrong_move img{
    width :400px;
    mix-blend-mode: lighten;
    border-radius: 20px;
}
.go-back{
    text-align: center;
    padding: 10px;
    margin-top: 20px;
    background-color: #ec9edc;
    color: rgba(15, 15, 15, 0.868);
    border: none;
    border-radius: 10px;
    cursor: pointer;
    justify-content: center;

}
.last-row {
    display: flex;
    flex-direction: row;
}

.book-button {
    padding: 5px 15px;
    border-radius: 10px;
    color: rgb(69, 84, 182);
    transition-delay: 0.3s;
    background-color: rgb(192, 140, 201);
}

.book-button:hover {
    color: white;
    transition-delay: 0.2s;
    background-color: #2E236C;
}

.section2 {
    width: 100%;
    height: 100%;
    display: contents;
    justify-content: center;
    align-items: center;
    background-color: #2E236C;
}

.pdf-container {
    height: 100%;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    background-color: #2E236C;
    padding: 20px;
    border-radius: 10px;
}

.pdf-viewer {
    width: 100%;
    height: 100%;
    border: none;
}

.pdf-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.pdf-viewer {
    width: 100%;
    height: 100%;
}

.pdf-overlay {
    position: absolute;
    top: 26px;
    right: 80px;
    width: 16%;
    height: 7%;
    background: rgba(255, 255, 255, 0);
    z-index: 10;
}


.rating-form {
    width: 100%;
    margin: 20px;
    padding: 20px;
    background-color: #2E236C;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.rating-form h3 {
    font-size: 24px;
    margin-bottom: 20px;
}

.rating-form .form-group {
    margin-bottom: 15px;
}

.rating-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.rating-form .stars {
    display: flex;
}

.rating-form .fa-star {
    font-size: 24px;
    cursor: pointer;
    color: #ccc;
}

.rating-form .fa-star.checked {
    color: gold;
}

.rating-form textarea {
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
}

.rating-form button {
    padding: 10px 20px;
    border-radius: 5px;
    background-color: rgb(16, 33, 110);
    color: white;
    border: none;
    cursor: pointer;
}

.rating-form button:hover {
    background-color: #2837ad;
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

.user-name {
    font-weight: bold;
}

.stars {
    display: inline-block;
}

.fa-star {
    font-size: 20px;
    cursor: pointer;
}

.rating-description {
    margin-top: 10px;
    font-style: italic;
}

/* gold button */
.golden-btn+.golden-btn {
    margin-top: 1em;
}

.golden-btn {
    display: inline-block;
    outline: none;
    margin: 10px;
    font-family: inherit;
    font-size: 1em;
    box-sizing: border-box;
    border: none;
    border-radius: .3em;
    height: 2.75em;
    line-height: 2.5em;
    text-transform: uppercase;
    padding: 0 1em;
    box-shadow: 0 3px 6px rgba(0, 0, 0, .16), 0 3px 6px rgba(110, 80, 20, .4),
        inset 0 -2px 5px 1px rgba(139, 66, 8, 1),
        inset 0 -1px 1px 3px rgba(250, 227, 133, 1);
    background-image: linear-gradient(160deg, #a54e07, #b47e11, #fef1a2, #bc881b, #a54e07);
    border: 1px solid #a55d07;
    color: rgb(120, 50, 5);
    text-shadow: 0 2px 2px rgba(250, 227, 133, 1);
    cursor: pointer;
    transition: all .2s ease-in-out;
    background-size: 100% 100%;
    background-position: center;
}

.golden-btn:focus,
.golden-btn:hover {
    background-size: 150% 150%;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.19), 0 6px 6px rgba(0, 0, 0, 0.23),
        inset 0 -2px 5px 1px #b17d10,
        inset 0 -1px 1px 3px rgba(250, 227, 133, 1);
    border: 1px solid rgba(165, 93, 7, .6);
    color: rgba(120, 50, 5, .8);
}

.golden-btn:active {
    box-shadow: 0 3px 6px rgba(0, 0, 0, .16), 0 3px 6px rgba(110, 80, 20, .4),
        inset 0 -2px 5px 1px #b17d10,
        inset 0 -1px 1px 3px rgba(250, 227, 133, 1);
}
</style>
