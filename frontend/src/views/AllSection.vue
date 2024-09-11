<!-- eslint-disable prettier/prettier -->
<template>
    <div class="book-row">
        <h3>All Books</h3>
        <div v-if="sections.length" class="section-column">
            <div v-for="section in sections" :key="section.id"  class="section-value">
                <div class="All_section_images"><img :src="getSectionImage(section.section_profile_image)" alt="Profile Image" class="All_section_profile-image" @click="selectBook(section.id)"/></div>
                <div class="section-info">
                    <router-link :to="{ name: 'SectionPage', params: { sectionId: section.id } }"><p class="sectionName">{{ section.name }}</p></router-link>
            </div>
            </div>
        </div>
        <div v-else>
            <p>No sections found.</p>
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
                .get('/AllSection',{
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

h3{
    font-size: 40px;
    padding-left: 40px;
    padding-top: 20px;
    color:white;
    font-weight: bold;
    font-family: Inter, sans-serif;
}
.sectionName{
    font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 20px;
    text-decoration: none;
    color:rgb(63, 63, 63);
}
.All_section_images{
    margin: 20px;
    height: 200px;
    width: 200px;
}
.All_section_profile-image{
    width: fit-content;
    height: 200px;
    border-radius: 50%;
}
.section-column{
    display: flex;
    padding:10px;
    flex-direction: row;
}
.section-value{
    margin-right: 30px;
}
.section-info{
    text-align: center;
    text-decoration: none;
    padding:10px;
    font-size: 35px;
}
a {
    color: inherit;
    text-decoration: none;
}

</style>