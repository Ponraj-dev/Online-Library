<!-- eslint-disable prettier/prettier -->
<template>
    <div>
        <data class="div1">
            <div class="search-bar">
                <select v-model="selectedCategory" class="categories">
                    <option value="">All Categories</option>
                    <option value="Adventure">Adventure</option>
                    <option value="Fantasy">Fantasy</option>
                    <option value="Historical">Historical</option>
                    <option value="Horror">Horror</option>
                    <option value="Mystery">Mystery</option>
                    <option value="Romance">Romance</option>
                    <option value="Thriller">Thriller</option>
                    <option value="Biography">Biography</option>
                    <option value="Non-Fiction">Non-Fiction</option>
                    <option value="Drama">Drama</option>
                </select>
                <input v-model="searchQuery" type="text" placeholder="Find the book you like..." />
                <button @click="searchBookSection">Search</button>
            </div>
        </data>
        <div v-if="All_books.length" class="Available_book">
            <div v-for="ebook in All_books" :key="ebook.id">
                <div class="add-ebook-info">
                    <img :src="getUserImage(ebook.profile_image)" alt="Profile Image"
                        class="add-image profile-image-book" />
                    <p class="add-bookname">{{ ebook.bookname }}</p>
                    <p class="authors"> {{ ebook.Authors }}</p>
                    <p v-if="ebook.in_section">already in</p>
                    <button v-if="isAdmin && !ebook.in_section" @click="addbook(ebook.id)"
                        class="book-button">add</button>
                    <button v-if="isAdmin && ebook.in_section" @click="removebook(ebook.id)"
                        class="book-button">remove</button>
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
            All_books: [],
            searchQuery: '',
            selectedCategory: '',
            isAdmin: localStorage.getItem('userRole') == "admin",
        };
    },
    name: "AddBooks",
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ''; // Optionally provide a placeholder image
        },
        fetchBookDetails() {
            let token = localStorage.getItem('accessToken');
            const sectionId = this.$route.params.sectionId || ''

            axios
                .get(`/AddBooksToSection/${sectionId}`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.All_books = response.data.ebooks_data;
                })
                .catch((error) => {
                    console.error("There was an error fetching the users!", error);
                });
        },
        addbook(bookid) {
            const token = localStorage.getItem('accessToken');
            const sectionId = this.$route.params.sectionId || ''

            axios.post('/addbook', { sectionId, bookid }, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then(() => {
                    this.All_books = this.All_books.map(ebook => {
                        if (ebook.id === bookid) {
                            ebook.in_section = true;
                        }
                        return ebook;
                    });
                })
                .catch((error) => {
                    console.error('There was an error adding the book!', error);
                });
        },
        removebook(bookid) {
            const token = localStorage.getItem('accessToken');
            const sectionId = this.$route.params.sectionId || ''

            axios.post('/removebook', { sectionId, bookid }, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then(() => {
                    this.All_books = this.All_books.map(ebook => {
                        if (ebook.id === bookid) {
                            ebook.in_section = false;
                        }
                        return ebook;
                    });
                })
                .catch((error) => {
                    console.error('There was an error removing the book!', error);
                });
        },
        searchBookSection() {
            let token = localStorage.getItem('accessToken');
            const sectionId = this.$route.params.sectionId || '';
            const searchParams = {
                category: this.selectedCategory,
                query: this.searchQuery,
                sectionId: sectionId
            };

            axios
                .get('/searchBooks', {
                    params: searchParams,
                    headers: {
                        "Content-Type": "application/json",
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.All_books = response.data.ebooks_data;
                })
                .catch((error) => {
                    console.error('There was an error searching for books!', error);
                });
        }

    },
    created() {
        this.fetchBookDetails();
    }
};
</script>
<!-- eslint-disable prettier/prettier -->
<style>
.div1 {
    display: flex;
    padding: 20px;
    margin: 20px;
    background-color: rgb(228, 228, 228);
    border-radius: 10px;
    width: 180vh;
}

.Available_book {
    padding: 20px;
    display: flex;
    flex-wrap: wrap;
    margin: 20px;
    background-color: rgb(228, 228, 228);
    border-radius: 10px;

}

.profile-image-book {
    width: 200px;
    height: auto;
    margin: 0;
}

.add-ebook-info {
    text-align: center;
    align-items: center;
    border-radius: 10px;
    box-shadow: 0 0 10px rgb(0, 0, 0);
    padding: 20px;
    margin: 20px;
    width: 30vh;
    height: 60vh;
}

.add-image {
    width: 25vh;
    height: 35vh;
}

.add-bookname {
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 20px;
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
.buttons {
    display: flex;
    max-width: fit-content;
    align-content: center;
    flex-direction: row;
    justify-content: space-around;
    margin-top: 20px;
}

.read {
    text-decoration: none;
    text-decoration-style: none;
    font-style: normal;
    color: rgb(51, 64, 82);
}

p {
    padding-left: 20px;
    padding-top: 9px;
    margin-bottom: 1px;
}

.read:hover {
    font-size: large;
    font-weight: bold;
}

.section2 {
    width: 100vh;
    height: 100vh;
    display: contents;
    justify-content: center;
    align-items: center;
    background-color: white;

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
</style>