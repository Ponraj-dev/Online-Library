<!-- eslint-disable prettier/prettier -->
<template>
    <div>
    <div class="admin-dashboard" v-if="isAdmin">
        <h3>Admin Dashboard</h3>

        <div class="appData">
            <div class="card">
                <div class="col">
                    <p>Users</p>
                    <i class="fa-solid fa-user"></i>
                </div>
                <div class="sub-col">{{ user_count }}</div>
                <div class=" col col1">
                    <router-link class="viewMore" to="/AllUsers"><p class="viewMore">View more. </p></router-link>

                </div>
            </div>
            <div class="card">
                <div class="col">
                    <p>books</p> <i class="fa-solid fa-book"></i>
                </div>
                <div class="sub-col">{{ book_count }}</div>
                <div class=" col col1">
                    <router-link class="viewMore" to="/AllBooks"><p class="viewMore">View more. </p></router-link>
                </div>
            </div>
            <div class="card">
                <div class="col">
                    <p>section</p> <i class="fa-solid fa-user"></i>
                </div>
                <div class="sub-col">{{ section_count }}</div>
                <div class=" col col1">
                    <router-link class="viewMore" to="/AllSection"><p class="viewMore">View more. </p></router-link>
                </div>
            </div>
            <div class="card">
                <div class="col">
                    <p>downloads</p> <i class="fa-solid fa-user"></i>
                </div>
                <div class="sub-col">0</div>
                <div class=" col col1">
                    <router-link class="viewMore" to="/downloads"><p class="viewMore">View more. </p></router-link>
                </div>
            </div>
        </div>

        <div class="charts">
            <div class="chart">
                <line-chart-vue />
            </div>
            <div class="chart2">
                <ratings-chart />
            </div>
        </div>
        <div class="row3">
            <div class="chart3">
                <bookslovedchart />
                <div class="report" v-if="isAdmin && isAuthenticated ">
                    <button  class="button" @click="triggerReport">Export Report</button>
                    <div v-if="taskStatus" class="button success">
                        Task Status: {{ taskStatus }}
                    </div>
                </div>
            </div>
                <div class="table-container " >
                    <p class="header-card">User's Table</p>
                    <div v-if="users.length" class="table-wrapper">
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>Profile</th>
                                    <th>Username</th>
                                    <th>Books</th>
                                    <th v-if="isAdmin">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="user in users" :key="user.id">
                                    <td class="profile-column" >
                                        <div class="profile-wrapper">
                                            <img :src="getUserImage(user.profile_image)" alt="Profile Image"
                                                class="profile-image" />
                                            <span v-if="user.is_logged_in" class="status online"></span>
                                            <span v-else class="status offline"></span>
                                        </div>
                                    </td>
                                    <td>
                                        <router-link :to="{ name: 'profile', params: { userId: user.id } } " class="name1">
                                            <p >{{ user.username }}</p>
                                        </router-link>
                                    </td>
                                    <td>{{ user.book_count }}</td>
                                    <td v-if="isAdmin">
                                        <button @click="deleteUser(user.id)" class="delete-button">Delete</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div v-else>
                        <p>No users found.</p>
                    </div>
                </div>
        </div>

    </div>
    <div v-else >
        <div class="wrong_move">
            <div> <h1>Unwanted move</h1></div>
        <div><img src="../assets/worng_move.gif" alt="profile" ></div>
        <div><button @click="goBack" class="go-back">Go Back</button></div>

        </div>
    </div>
    </div>

</template>
<!-- eslint-disable prettier/prettier -->

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from 'axios';
import lineChartVue from '../components/lineChart.vue';
import Bookslovedchart from '../components/bookslovedchart.vue';
import RatingsChart from '../components/ratingsChart.vue';

export default {
    data() {
        return {
            users: [],
            isAdmin: localStorage.getItem('userRole') === 'admin',
            isAuthenticated : localStorage.getItem('accessToken'),
            requestCounts: [],
            user_count:"",
            book_count:"",
            section_count:"",
            taskStatus: null,
            taskId: null
        };
    },components: {
        lineChartVue,
        Bookslovedchart,
        RatingsChart
    },
    name: 'Dashboard',
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            // Provide a default placeholder image
            return '/default-profile-image.jpg';
        },
        fetchUsers() {
            const token = localStorage.getItem('accessToken');
            axios
                .get('/adminDashboard', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.users = response.data.users;
                    this.user_count = response.data.User_count;
                    this.book_count = response.data.Book_count;
                    this.section_count = response.data.Section_count
                })
                .catch((error) => {
                    console.error('There was an error fetching the users!', error);
                    // Optionally handle the error in the UI, e.g., show a notification
                });
        },
        goBack() {
            this.$router.go(-1); // This navigates the user back to the previous page
        },
        deleteUser(userId) {
            const token = localStorage.getItem('accessToken');
            axios
                .delete(`/delete_user/${userId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                })
                .then(() => {
                    this.fetchUsers();
                })
                .catch((error) => {
                    console.error('There was an error deleting the user!', error);
                    // Optionally handle the error in the UI, e.g., show a notification
                });
        },
        async triggerReport() {
            try {
                const response = await axios.post('http://localhost:5000/api/trigger_report');
                if (response.status !== 202) {
                    throw new Error('Network response was not ok');
                }
                this.taskId = response.data.task_id;
                if (this.taskId){
                    this.taskStatus="book downloaded"
                }
                this.checkStatus();
            } catch (error) {
                console.error('Error triggering report:', error);
            }
        },
        async checkStatus(taskId ) {
            try {
                if (taskId  !== None) {
                    console.log('Task completed:', data.result);
                }
            } catch (error) {
                console.error('Error checking status:', error);
            }
        },
    },
    created() {
        this.fetchUsers();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->

<style scoped>
.admin-dashboard {
    padding: 20px;
}
.viewMore{
    text-decoration: none;
}
.viewMore:hover{
    color: rgb(0, 238, 255);
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
h3{
    font-size: 40px;
    color:white;
    font-weight: bold;
    font-family: Inter, sans-serif;
}
h1{
    font-size: 90px;
    color:white;
    font-weight: bold;
    font-family: Inter, sans-serif;
}
.appData {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    width: 100%;
    justify-content: space-around;
    margin-bottom: 20px;
}

.logo {
    font-size: 20px;
}
.header-card{
    font-size: 30px;
    width:100%;
    border-bottom: 1px solid rgba(107, 104, 169, 0.803);
}
.card {
    background-color: #2E236C;
    color: white;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 50px;
    color: #333;
    flex: 1 1 23%;
    min-width: 200px;
    padding: 20px;
    box-sizing: border-box;
    transition: transform 0.3s ease-in-out;

}

.card:hover,
.chart:hover ,
.chart2:hover,
.chart3:hover  {
    transform: translateY(-10px);
}

.user-card {
    display: flex;
    align-items: center;
    flex-direction: row;
    padding: 10px;
    margin: 20px;
    justify-content: space-around;
}

.ActiveStatus {
    position: relative;
    display: inline-block;
    margin: 10px;
}

.charts {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}

.col,
.sub-col {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    font-weight: bold;
}

.sub-col {
    padding-left: 20px;
    font-size: 50px;
    color: white;
}


.col p,
i {
    align-items: center;
    font-size: 20px;
    color: rgb(90, 151, 159);
}
.col1 p{
    font-size: 15px;
    color: rgb(90, 151, 159);
}
.col1{
    align-items: center;
    justify-content: flex-end;
}
.chart {
    display: flex;
    align-items: center;
    width: 400px;
    height: 500px;
    margin-right: 20px;
    flex: 1 1 30%;
    transition: transform 0.3s ease-in-out;

}

.chart2 {
    margin-right: 10px;
    width: 500px;
    height: 500px;
    display: flex;
    align-items: center;
    flex: 1 1 23%;
    transition: transform 0.3s ease-in-out;

}

.chart3 {
    display: flex;
    align-items: center;
    flex-direction: column;
    width: 800px;
    height: 400px;
    margin-right: 20px;
    flex: 1 1 20%;
    transition: transform 0.3s ease-in-out;
}
.report{
    display: flex;
    border-radius: 20px;
    width: 100%;
    padding:30px;
    margin-top: 20px;
    text-decoration: none;
    background-color: #2E236C;
    color: #fff;
}

.row3 {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    flex: 1 1 30%;
    margin-top: 20px;
}

.profile-image {
    width: 60px;
    height: 60px;
    border-radius: 50%;
}

.online {
    position: absolute;
    width: 20px;
    height: 20px;
    margin-right: 20px;
    border-radius: 50%;
    z-index: 10;
}

.online {
    position: absolute;
    width: 6px;
    height: 6px;
    /* White border for better visibility */
    background-color: rgba(102, 101, 101, 0);
    border: 6px solid rgb(45, 230, 38);
    border-radius: 50%;
    bottom: 0px;
    /* Positioning it at the bottom right corner */
    right: -5px;
    z-index: 10;
}

.offline {
    position: absolute;
    width: 6px;
    height: 6px;
    /* White border for better visibility */
    background-color: rgba(218, 218, 218, 0.958);
    border: 5px solid rgba(76, 76, 76, 0.509);
    border-radius: 50%;
    bottom: 0px;
    /* Positioning it at the bottom right corner */
    right: 10px;
    z-index: 10;
}

.delete-button {
    margin-left: 10px;
    background-color: red;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
}
.button{

    color:white;
    padding:20px;
    text-decoration: none;
    background-color: #130f2a;
    border: 1px solid white;
    border-radius: 20px;
    color: #ffffff;
    font-weight: bold;
}

.success{
    margin-left:30px ;
    background-color: #42bb54;
}

.table-container {
    width: 100%;
    max-height: 600px; /* Adjust based on your preference */
    overflow-y: auto; /* Enable vertical scrolling */
    background-color: #2E236C;
    border-radius: 10px;
    padding: 20px;
    box-sizing: border-box;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 20px;
    flex: 1 1 23%;
    min-width: 200px;
    color:white;
}

.table-wrapper {
    overflow-x: auto;
}
.name1{
    text-decoration: none;
    color:white;
}
.styled-table {
    width: 100%;
    border-collapse: collapse;
}

.styled-table thead tr {
    background-color: #433D8B;
    color: #fff;
    text-align: left;
}

.styled-table th, .styled-table td {
    padding: 12px 15px;
}

.styled-table tbody tr {
    border-bottom: 1px solid #333a56;
}

.styled-table tbody tr:last-of-type {
    border-bottom: 2px solid #333a56;
}

.styled-table tbody tr:hover {
    background-color: #3c3e58;
}

.profile-column {
    display: flex;
    align-items: center;
}

.profile-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.profile-image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
}

</style>
