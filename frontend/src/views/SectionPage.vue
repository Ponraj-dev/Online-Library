<!-- eslint-disable prettier/prettier -->
<template>
    <div v-if="sections.length" class="Ebook-column">
        <div v-for="ebook in sections" :key="ebook.id" class="section1">
            <img :src="getUserImage(ebook.section_profile_image)" alt="Profile Image" class="profile-image-section" />
            <div class="ebook-info">
                <p class="name">{{ ebook.name }}</p>
                <p class="description">{{ ebook.description }}</p>
                <button v-if="isAdmin" @click="deleteSection(ebook.id)" class="book-button">Delete</button>
                <button v-if="isAdmin" @click="editSection(ebook.id)" class="book-button">Edit</button>
                <router-link v-if="isAdmin" :to="{ name: 'AddBooks', params: { sectionId: ebook.id } } " class="book-button-add">
                <p class="book-button1">Add books</p>
                </router-link>
            </div>

        </div>
        <div class="sub-section2">
                <div v-for="ebook in ebooks" :key="ebook.id" class="sub-book-info" >
                    <img :src="getUserImage(ebook.Book_image)" alt="Profile Image" class="sec-profile-image-book" />
                    <p class="sub-name">{{ ebook.title }}</p>
                    <button v-if="!isAdmin && ebook.status === 'Available' && !ebook.pending" @click="RequestBook(ebook.id)" class="book-button">Request</button>
                    <button v-if="ebook.issued && !isAdmin && ebook.status === 'Issued'" @click="ReturnBook(ebook.id)" class="book-button">Return</button>

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
            sections: [],
            ebooks: [],
            isAdmin: localStorage.getItem('userRole') == "admin",

        };
    },
    name: "SectionsPage",
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ''; // Optionally provide a placeholder image
        },
        getBookpdf(base64PDF) {
            if (base64PDF) {
                return `data:application/pdf;base64,${base64PDF}`;
            }
            return ''; // Optionally provide a placeholder
        },
        fetchSections() {
            let token = localStorage.getItem('accessToken');
            const sectionId = this.$route.params.sectionId || ''
            this.selectedBook = sectionId

            axios
                .get(`/sectionspage/${sectionId}`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.sections = response.data.sections;
                    this.ebooks = response.data.ebooks;
                })
                .catch((error) => {
                    console.error("There was an error fetching the users!", error);
                });
        },
        deleteSection(sectionId) {
            let token = localStorage.getItem('accessToken');
            axios
                .delete(`/deletesection/${sectionId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                })
                .then(() => {
                    this.$router.push("/dashboard");

                })
                .catch((error) => {
                    console.error("There was an error deleting the user!", error);
                });
        },
        removeBook(sectionId) {
            const token = localStorage.getItem('accessToken');
            axios.post("/removebook", { sectionId }, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then(() => {
                    this.$router.push("/sectionPage");
                })
                .catch((error) => {
                    console.error('There was an error returning the book!', error);
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
        },
        editSection() {
            const sectionId = this.$route.params.sectionId || ''
            this.$router.push(`/Editsections/${sectionId}`);
        },
    },
    created() {
        this.fetchSections();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style>
.sub-section2 {
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    margin: 20px;
    margin: 30px;
    background-color: #110b2d96;
    border-radius: 10px;
    width: 180vh;
}
.sub-book-info{
    justify-content: center;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.877);
    border-radius: 20px;
    margin: 10px;
    padding: 20px;
    border-radius: 10px;
    width: 30vh;
}
.description{
    width: 60%;
    font-size: 20px;
}
.sub-book-info:hover{
    background-color: #C8ACD6;
    color: #110b2d96;
}
p.name{
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 50px;
}


.imageView {
    width: 90%;
    height: 200px;
    overflow: hidden;
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
.sec-profile-image-book{
    width: 190px;
    height: auto;
}

.Ebook-column {
    height: 100%;
}

.profile-image-section {
    width: 200px;
    height: 200px;
    padding:20px;
    border-radius: 50%;
}
.book-button-add{text-decoration: none
}

.sub-name {
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 20px;
}

.book-button {
    padding: 5px 15px;
    border-radius: 10px;
    background-color: rgba(240, 248, 255, 0.125);
    border: 2px solid rgb(255, 255, 255);
    cursor: pointer;
    margin: 10px;
}
.book-button1{
    padding: 5px 15px;
    border-radius: 10px;
    background-color: rgb(230, 163, 213);
    margin: 10px;
    cursor: pointer;
    width:30%;
}
.book-button:hover {
    color: rgb(85, 90, 125);
    transition-delay: 0.3s;
    background-color: rgb(37, 28, 97);
}

</style>