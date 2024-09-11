<!-- eslint-disable prettier/prettier -->
<template>
    <div class="edit-form-container">
        <h3>Edit Section </h3>
        <div class="EditSection">
            <form @submit.prevent="Editsections" class="edit-form-left">
            <div >
                <input type="text" id="name" v-model="name" required>

                <div id="genre" class="genre">
                    <div v-for="genre in availableGenres" :key="genre" class='sub-genre'>
                        <input type="checkbox" :id="genre" :value="genre" v-model="genres" />
                        <label :for="genre">{{ genre }}</label>
                    </div>
                </div>

                <label for="image" class="custom-file-upload">Cover Page | {{ imageName }}</label>
                <input type="file" id="image" @change="onCoverImage">

                <textarea type="text" class="description" id="description" v-model="description"
                required></textarea>

                <button type="submit">Create</button>
            </div>
            </form>
        <div class="edit-form-right">
            <div class="imageView1">
                    <img v-if="imageUrl" :src="imageUrl" alt="Profile Image Preview" class="image-preview" />
                    <img v-else :src="getSectionImage(imageCode)" alt="Profile Image" class="profile-page-image" />
                </div></div>
        <p v-if="message">{{ message }}</p>
    </div></div>
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
            imageCode:""
        };
    },
    name: "Editsections",
    methods: {
        onCoverImage(event) {
            this.image = event.target.files[0];
            this.imageUrl = URL.createObjectURL(this.image);
            this.imageName = this.image.name;
        },
        getSectionImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return "";
        },
        Editsections() {
            let formData = new FormData();
            const sectionId = this.$route.params.sectionId || '';
            let token = localStorage.getItem('accessToken');

            formData.append("name", this.name);
            formData.append("genre", this.genres.join(','));
            formData.append("image", this.image);
            formData.append("description", this.description);

            axios.post(`/Editsection/${sectionId}`, formData, {
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
                    this.description= "",
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
        },fetchSection() {
            const sectionId = this.$route.params.sectionId || '';
            let token = localStorage.getItem("accessToken");

            axios
                .get(`/Editsection/${sectionId}`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        Authorization: `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    const section = response.data.section;
                    this.name = section.name;
                    this.description=section.description
                    this.imageCode = section.image
                })
                .catch((error) => {
                    console.error("There was an error fetching the book!", error);
                });
        },
    },
    created() {
        this.fetchSection();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
.edit-form-container {

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
.EditSection{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;

}
.edit-form-left,.edit-form-right{
    border-radius: 10px;
    box-shadow: 0 0 10px rgb(0, 0, 0);
    background-color: #2E236C;
    padding: 20px;
    margin: 40px;
    flex: 1 1 60%;
}
.edit-form-right{
    padding: 0px;
    flex: 1 1 33%;
}
.edit-form-container input,textarea,
.edit-form-container button {
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
.edit-form-right ,.imageView{
    height: 400px;
    overflow: hidden;
}

.imageView1 img {
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

