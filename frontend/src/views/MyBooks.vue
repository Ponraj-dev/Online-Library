<!-- eslint-disable prettier/prettier -->
<template>
    <div v-if="my_books.length" class="Ebook-column">
        <div v-for="ebook in my_books" :key="ebook.id" class="section1" >
            <img :src="getUserImage(ebook.profile_image)" alt="Profile Image" class="profile-image-book" />
            <div class="ebook-info">
                <p class="bookname">{{ ebook.bookname }}</p>
                <p class="authors">written by : {{ ebook.Authors }}</p>
                <p class="authors"> {{ ebook.description }}</p>
                <div class="buttons">
                    <button @click="ReturnBook(ebook.id)" class="book-button">Return</button>
                    <router-link :to="{ name: 'EbookPage', params: { bookId: ebook.id } } " class="read"> <p class="readWord">Read</p></router-link>
                </div>
            </div>

        </div>
    </div>
    <div v-else>
        <p>No books found.</p>
    </div>


</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from "axios";

export default {
    data() {
        return {
            my_books: [],
            isAdmin: localStorage.getItem('userRole') == "admin",

        };
    },
    name: "MyBooks",
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ''; // Optionally provide a placeholder image
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
        },
    },
    created() {
        this.fetchBookDetails();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style>
.section1 {
    display: flex;
    flex-wrap: nowrap;
    padding: 20px;
    margin: 20px;
    background-color: #2E236C;
    border-radius: 10px;
    width: 100%;
    align-items: center;
}
.Ebook-column{
    height:100%;
}
.profile-image-book {
    margin-right: 20px;
}

.bookname {
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 50px;
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
    color: white;
    transition-delay: 0.3s;
    background-color: rgb(16, 33, 110);
}
.buttons{
    display: flex;
    max-width: fit-content;
    align-content: center;
    flex-direction: row;
    justify-content: space-around;
    margin-top: 20px;
}
.readWord{
    text-decoration-style: none;
    font-size: 20px;
    color:rgba(90, 187, 187, 0.929)
}
.read{
    padding:10px;
    text-decoration: none;
    text-decoration-style: none;
    font-style: normal;
    font-size: medium;
    color:rgba(90, 187, 187, 0.929)
}
p{
    padding-left: 20px;
    padding-top: 9px;
    margin-bottom: 1px;
}
.read:hover{
    color:rgba(0, 255, 255, 0.719);
}
.section2 {
    width: 100vh;
    height:  100vh;
    display: contents;
    justify-content: center;
    align-items: center;
    background-color: white;

}

.pdf-container {
    height: 100%;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 10px;
}

.pdf-viewer {
    width: 100%;
    height: 100%;
    border: none;
}

@media (max-width: 768px) {
    .section1 {
    display: flex;
    flex-wrap: wrap;
    }
}
</style>