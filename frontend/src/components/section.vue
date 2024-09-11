<!-- eslint-disable prettier/prettier -->
<template>
    <div class="book-row">
        <div v-if="sections.length" class="section-column">
            <div v-for="section in sections" :key="section.id"  class="section-value">
                <div class="section_images"><img :src="getSectionImage(section.section_profile_image)" alt="Profile Image" class="profile-image" @click="selectBook(section.id)"/></div>
                <div class="section-info">
                    <router-link :to="{ name: 'SectionPage', params: { sectionId: section.id } }"><h4 class="sectionName">{{ section.name }}</h4></router-link>
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
            sections: [],
        };
    },
    name: "sections",
    methods: {
        getSectionImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ''; // Optionally provide a placeholder image
        },
        selectBook(sectionId) {
        this.$emit('book-selected', sectionId);
        },
        fetchUsers() {
            let token = localStorage.getItem('accessToken');

            axios
                .get('/sectionsDashboard',{
                headers: {
                    "Content-Type": "multipart/form-data",
                    'Authorization':`Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then((response) => {
                    this.sections = response.data.sections;
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

.book-row {
    display: flex;
    flex-direction: column;
    align-self: start;
    padding: 20px;

}
.section_images img{
    height: 100px;
    width: 100px;
}
.sectionName{
    font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 20px;
    font-weight: bold;
    text-decoration: none;
    color:rgb(63, 63, 63);
    text-align: center;
    padding-left: None ;
    padding-top: 10px;
}
.sectionName:hover{
    color:rgba(0, 255, 255, 0.719);
}
.profile-image{
    width: fit-content;
    height: 100px;
    border-radius: 100px;;
}
.section-column{
    display: flex;
    padding:10px;
    flex-direction: row;
    text-align: center;
}
.section-value{
    margin-right: 30px;
}
.bookname{
    text-decoration: none;
    padding:20px;
    font-size: 15px;
}
a {
    color: inherit;
    text-decoration: none;
}

</style>