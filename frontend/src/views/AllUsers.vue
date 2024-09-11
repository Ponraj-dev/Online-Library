<!-- eslint-disable prettier/prettier -->
<template>

    <div class="table-container ">
        <h3 class="header-card">User's Table</h3>
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
                        <td class="profile-column">
                            <div class="profile-wrapper">
                                <img :src="getUserImage(user.profile_image)" alt="Profile Image"
                                    class="profile-image" />
                                <span v-if="user.is_logged_in" class="status online"></span>
                                <span v-else class="status offline"></span>
                            </div>
                        </td>
                        <td>
                            <router-link :to="{ name: 'profile', params: { userId: user.id } }" class="name1">
                                <p>{{ user.username }}</p>
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
</template>
<!-- eslint-disable prettier/prettier -->

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from 'axios';
export default {
    data() {
        return {
            users: [],
            isAdmin: localStorage.getItem('userRole') === 'admin',
        };
    },
    name: 'AllUsers',
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
                .get('/AllUsers', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.users = response.data.users;
                })
                .catch((error) => {
                    console.error('There was an error fetching the users!', error);
                    // Optionally handle the error in the UI, e.g., show a notification
                });
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
    },
    created() {
        this.fetchUsers();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->

<style scoped>

.row3 {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    flex: 1 1 30%;
    margin-top: 20px;
}
h3 .header-card{
    font-size: 40px;
    padding-top: 20px;
    color:white;
    font-weight: bold;
    font-family: Inter, sans-serif;
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



.table-container {
    width: 100%;
    /* Adjust based on your preference */
    overflow-y: auto;
    margin: 20px;
    /* Enable vertical scrolling */
    background-color: #2E236C;
    border-radius: 10px;
    padding: 20px;
    box-sizing: border-box;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 20px;
    flex: 1 1 23%;
    color: white;
}

.table-wrapper {
    overflow-x: auto;
}

.name1 {
    text-decoration: none;
    color: white;
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

.styled-table th,
.styled-table td {
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
