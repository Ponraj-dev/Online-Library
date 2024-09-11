<!-- eslint-disable prettier/prettier -->
<template>
    <div class="form-container">
        <h3>Edit Book</h3>
        <form @submit.prevent="editBook">
            <div class="edit-page">
                <div class="form-left">
                    <label for="bookname">Book Name</label>
                    <input type="text" id="bookname" v-model="bookname" required>
                    <label for="authors">Authors</label>
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
                    <input type="file" id="image" @change="onCoverImageChange" >
                    <div class="imageView">
                        <p class="name1">Preview Image</p>
                        <img v-if="imageUrl" :src="imageUrl" alt="Profile Image Preview"
                            class="image-preview-edit" />
                            <img v-else :src="getBookImage(imageCode)" alt="Profile Image" class="profile-page-image" />
                            </div>
                    <br>
                    <label for="book" class="custom-file-upload">Book Page | {{ bookName }} </label>
                    <input type="file" id="book" @change="onBookFileChange" >
                    <textarea type="text" class="description" id="description" v-model="description"
                        required></textarea>
                    <button type="submit">Save Changes</button>
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
            authors: "",
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
            ],
            description: "",
            image: null,
            book: null,
            message: "",
            ebook: {},
            imageUrl: null,
            imageName:"",
            bookName:"",
            imageCode:""
        };
    },
    name: "EditBook",
    methods: {
        onCoverImageChange(event) {
            this.image = event.target.files[0];
            this.imageUrl = URL.createObjectURL(this.image);
            this.imageName = this.image.name;
        },
        onBookFileChange(event) {
            this.book = event.target.files[0];
            this.bookName = this.book.name;
        },
        getBookImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return "";
        },
        editBook() {
            let formData = new FormData();
            const bookId = this.$route.params.bookId || '';
            let token = localStorage.getItem("accessToken");

            formData.append("bookname", this.bookname);
            formData.append("authors", this.authors);
            formData.append("genre", this.genres.join(','));
            formData.append("description", this.description);
            formData.append("image", this.image);
            formData.append("book", this.book);

            axios
                .post(`/EditBook/${bookId}`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        Authorization: `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.message = response.data.message;
                    this.bookname = "";
                    this.authors = "";
                    this.genre = "";
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
        fetchBook() {
            const bookId = this.$route.params.bookId || '';
            let token = localStorage.getItem("accessToken");

            axios
                .get(`/EditBook/${bookId}`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        Authorization: `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    const ebook = response.data.ebook;
                    this.bookname = ebook.bookname;
                    this.authors = ebook.authors;
                    this.genre = ebook.genre;
                    this.description = ebook.description;
                    this.book = ebook.book;
                    this.image = ebook.image;
                    this.imageCode= ebook.Book_profile_image
                })
                .catch((error) => {
                    console.error("There was an error fetching the book!", error);
                });
        },
    },
    created() {
        this.fetchBook();
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
    border-radius: 20px;
    margin: 10px;
}

.form-right {
    width: 26%;
    flex: 1 1 23%;
    padding: 40px;
    background-color: #2E236C;
    border-radius: 20px;
    margin: 10px;
}

.form-container input,
textarea,
.form-container button {
    display: flex;
    border: 3px solid #ffffffb3;
    background-color: #1b1443;
    padding: 10px;
    margin: 10px 0;
    border-radius: 20px;
    width: 90%;
    text-decoration: none;
    color:white;
}

.form-container button:hover {
    cursor: pointer;
    background-color: #3e35be;
    color: white;
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
    border: 3px solid #ffffffb3;
    background-color: #1b1443;
    padding: 10px;
    width: 90%;
    margin: 10px 0;
    border-radius: 20px;
    display: inline-block;
    cursor: pointer;
}

.description {
    height: 200px;
    padding-bottom: 20px;
}

.imageView {
    width: 100%;
    height: 200px;
    overflow: hidden;
    margin:10px;
    border: 3px solid #C8ACD6;
    border-radius: 20px;

}
.imageView img {


    height: 100%;
    /* Make image height 100% of the container */
    width: 100%;
    /* Maintain aspect ratio */
    object-fit: cover;
    /* Cover the container area */
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
        border: 3px solid #2837ad;
        background-color: #ffffff;
        border-radius: 20px;
        margin: 10px;
    }

    .form-right {
        width: 100%;
        border: 3px solid #2837ad;
        background-color: #ffffff;
        border-radius: 20px;
        margin: 10px;
    }

}
</style>
