<!-- eslint-disable prettier/prettier -->
<template>
    <div class="form-container">
    <h3>Book Creation</h3>

        <form @submit.prevent="bookCreation">
            <div class="edit-page">
                <div class="form-left">
                <label for="bookname">Book Name</label>
                <input type="text" id="bookname" v-model="bookname" placeholder="BookName" required>
                <label for="Authors">Authors</label>
                <input type="text" id="authors" v-model="authors" required>
                <label for="genre">Genre</label>
                <div id="genre" class="genre">
                    <div v-for="genre in availableGenres" :key="genre" class='sub-genre'>
                        <input type="checkbox" :id="genre" :value="genre" v-model="genres" />
                        <label :for="genre">{{ genre }}</label>
                    </div>
                </div>
                </div>
        <div class="form-right">
            <label for="image" class="custom-file-upload">Cover Page | {{ imageName }}</label>
            <input type="file" id="image" @change="onCoverImage" required>
            <div class="imageView2">
                <p class="name1">Preview Image</p>
                <img v-if="imageUrl" :src="imageUrl" alt="Profile Image Preview" class="image-preview" />
            </div>
                <br>
            <label for="book" class="custom-file-upload">Book Name | {{ bookName }}</label>
            <input type="file" id="book" @change="onBookFile" required>

            <textarea type="text" class="description" id="description" v-model="description" placeholder="Description" required></textarea>
            <button type="submit">create</button>
            </div>
            </div>
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
            bookname: "",
            genres: [],
            availableGenres: [
                "Adventure",
                "Fantasy",
                "Historical",
                "Horror",
                "Mystery",
                "Romance",
                "Thriller",
                "Biography",
                "Non-Fiction",
                "Drama"
            ]
            ,
            authors: "",
            description: "",
            image: null,
            message: "",
            book: null,
            imageUrl: null,
            imageName: "",
            bookName: "",
        };
    },
    methods: {
        onCoverImage(event) {
            this.image = event.target.files[0];
            this.imageUrl = URL.createObjectURL(this.image);
            this.imageName = this.image.name;
        },
        onBookFile(event) {
            this.book = event.target.files[0];
            this.bookName = this.book.name;
        },
        bookCreation() {
            let formData = new FormData();
            let token = localStorage.getItem('accessToken');


            formData.append("bookname", this.bookname);
            formData.append("authors", this.authors);
            formData.append("genre", this.genres.join(','));
            formData.append("description", this.description);
            formData.append("image", this.image);
            formData.append("book", this.book);

            axios.post('http://localhost:5000/api/bookcreation', formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    'Authorization': `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then((response) => {
                    this.message = response.data.message;
                    this.bookname = "";
                    this.genre = "";
                    this.authors = "";
                    this.description = "";
                    this.image = null;
                    this.book = null;
                    this.$router.push("/dashboard");
                })
                .catch((error) => {
                    if (error.response && error.response.data) {
                        this.message = error.response.data.message;
                    } else {
                        this.message = "An error occurred.";
                    }
                });
        },
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
.form-container {
    height:100%;
    overflow-y: auto;
}
h3{
    font-size: 40px;
    padding-left: 40px;
    padding-top: 20px;
    color:white;
    font-weight: bold;
    font-family: Inter, sans-serif;
}
.edit-page {
    width: 100%;
    margin: auto;
    padding: 20px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;

}

.form-left {
    width: 70%;
    padding: 30px;
    background-color: #2E236C;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.877);
    border-radius: 20px;
    margin: 10px;
    flex: 1 1 60%;
}

.form-right {
    width: 30%;
    padding: 40px;
    background-color: #2E236C;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.892);
    border-radius: 20px;
    margin: 10px;
    flex: 1 1 23%;
}

.form-container input,textarea,
.form-container button {
    display: flex;
    border: 3px solid #C8ACD6;
    background-color: #1e1b4ee0;
    padding: 10px;
    margin: 10px 0;
    border-radius: 20px;
    width: 90%;
    text-decoration: none;
    color:white;
}

.form-container button:hover {
    cursor: pointer;
    background-color: #141053;
    color: white;
}

.imageView2 {
    width: 90%;
    height: 200px;
    overflow: hidden;
    border: 3px solid #C8ACD6;
    border-radius: 20px;

}
.imageView2 img {


    height: 100%;
    /* Make image height 100% of the container */
    width: 100%;
    /* Maintain aspect ratio */
    object-fit: cover;
    /* Cover the container area */
}


.genre {
    display: flex;
    padding: 20px;
    flex-wrap: wrap;
    flex-direction: row;
}

.sub-genre {
    padding: 30px;
}

input[type="file"] {
    display: none;
}

.custom-file-upload {
    border: 3px solid #C8ACD6;
    background-color: #1e1b4ee0;
    padding: 10px;
    width:90%;
    margin: 10px 0;
    border-radius: 20px;
    display: inline-block;
    cursor: pointer;
}
.description{
    height:200px;
    padding-bottom:20px;
}

@media (max-width: 400px) {
    .edit-page {
        display: flex;
        flex-direction: column;
        width: fit-content;
        box-sizing: none !important;
    }

    .form-left {
        width: 100%;
        padding: 30px;
        border: 3px solid #C8ACD6;
        background-color: #2E236C;
        border-radius: 20px;
        margin: 10px;
    }

    .form-right {
        width: 100%;
        border: 3px solid #C8ACD6;
        background-color: #2E236C;
        border-radius: 20px;
        margin: 10px;
    }

}
</style>
