<!-- eslint-disable prettier/prettier -->
<template>
    <div class="create-form-container">
            <h3>Section Creation</h3>
        <div class="createSection">
        <form @submit.prevent="sectionCreation"  class="create-form-left" >
            <div>
                <input type="text" id="name" v-model="name" required placeholder="Section Name">

                <div id="genre" class="genre">
                    <div v-for="genre in availableGenres" :key="genre" class='sub-genre'>
                        <input type="checkbox" :id="genre" :value="genre" v-model="genres" />
                        <label :for="genre">{{ genre }}</label>
                    </div>
                </div>
                <label for="image" class="custom-file-upload">Cover Page | {{ imageName }}</label>
                <input type="file" id="image" @change="onCoverImage" required>

                <textarea type="text" class="description" id="description" placeholder="description" v-model="description" required></textarea>

                <button type="submit">Create</button>
            </div>
        </form>
        <div class="create-form-right">
            <p class="name1">Preview Image</p>
            <div class="imageView3">
                <img v-if="imageUrl" :src="imageUrl" alt="Profile Image Preview" class="image-preview" />
            </div>
        </div>
        <p v-if="message">{{ message }}</p>
    </div>
    </div>

</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from "axios";

export default {
    data() {
        return {
            name: "",
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
            image: null,
            description: "",
            imageName: "",
            imageUrl: null,
            message: "",
        };
    },
    name: "sectionCreation",
    methods: {
        onCoverImage(event) {
            this.image = event.target.files[0];
            this.imageUrl = URL.createObjectURL(this.image);
            this.imageName = this.image.name;
        },
        sectionCreation() {
            let formData = new FormData();
            let token = localStorage.getItem('accessToken');

            formData.append("name", this.name);
            formData.append("genre", this.genres.join(','));
            formData.append("image", this.image);
            formData.append("description", this.description);

            axios.post(`/sectionCreation`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    'Authorization': `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then((response) => {
                    this.message = response.data.message;
                    this.name = "";
                    this.genres = [];
                    this.image = null;
                    this.description = "",
                    this.imageName = "";
                    this.imageUrl = null;
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
.create-form-container {

    max-width: 100%;

}
h3{
    font-size: 40px;
    padding-left: 40px;
    padding-top: 20px;
    color:white;
    font-weight: bold;
    font-family: Inter, sans-serif;
}
form{
    max-width: 100vh;
}
.createSection{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;

}
.create-form-left,.create-form-right{
    border-radius: 10px;
    box-shadow: 0 0 10px rgb(0, 0, 0);
    background-color: #2E236C;
    padding: 20px;
    margin: 40px;
    flex: 1 1 60%;
}
.create-form-right{
    padding: 0px;
    flex: 1 1 33%;
}
.create-form-container input,textarea,
.create-form-container button {
    display: flex;
    border: 3px solid #C8ACD6;
    background-color: #1e1b4ee0;
    padding: 10px;
    margin: 10px 0;
    border-radius: 20px;
    width: 90%;
    text-decoration: none;
    color:#ffffff;
}

.form-container button:hover {
    cursor: pointer;
    background-color: #141053;
    color: white;
}
.create-form-right ,.imageView3{
    height: 400px;
    overflow: hidden;
}

.imageView3 img {
    height: 100%;
    width: 100%;
    object-fit: cover;

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
    width: 90%;
    margin: 10px 0;
    border-radius: 20px;
    display: inline-block;
    cursor: pointer;
}
.file-name {
    display: block;
    margin-top: 10px;
    color: #17153B;
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

