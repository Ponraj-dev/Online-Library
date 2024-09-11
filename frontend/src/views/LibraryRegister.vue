<!-- eslint-disable prettier/prettier -->
<template>
    <div class="tables">
        <div class="table1">
            <table v-if="requests.length" class="requests-table">
                <thead>
                    <tr>
                        <th>Request ID</th>
                        <th>Username</th>
                        <th>Requested Book</th>
                        <th>Date Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in requests" :key="request.id">
                        <td>{{ request.id }}</td>
                        <td>{{ request.requested_user_name }}</td>
                        <td>{{ request.requested_book }}</td>
                        <td>{{ request.requested_date }}</td>
                        <td>
                            <button v-if="!request.is_approved" @click="approveRequest(request.id)" class="book-button">Approve</button>
                            <button v-if="request.is_approved && !request.is_retrieved" @click="retrieveBook(request.id)" class="book-button">Retrieve</button>
                            <button v-if="!request.is_approved" @click="rejectRequest(request.id)" class="book-button">Reject</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-else>
                <p>No book requests found.</p>
            </div>
        </div>
        <div class="table2">
            <table v-if="issuedBooks.length" class="requests-table">
                <thead>
                    <tr>
                        <th>Approved ID</th>
                        <th>Username</th>
                        <th>Approved Book</th>
                        <th>Date of Approval</th>
                        <th>Due Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="issued in issuedBooks" :key="issued.id">
                        <td>{{ issued.id }}</td>
                        <td>{{ issued.issued_user_name }}</td>
                        <td>{{ issued.issuedBook_name }}</td>
                        <td>{{ issued.approved_date }}</td>
                        <td>{{ issued.due_date }}</td>
                        <td>
                            <button @click="retrieveBook(issued.id)" class="book-button">Retrieve</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-else>
                <p>No issued books found.{{ message }}</p>
            </div>
        </div>
    </div>
</template>
<!-- eslint-disable prettier/prettier --><script>
import axios from "axios";

export default {
    data() {
        return {
            requests: [],
            issuedBooks: [],
            message: "",
        };
    },
    name: "LibraryRegister",
    methods: {
        fetchRequests() {
            const token = localStorage.getItem('accessToken');
            axios.get("/libraryregister", {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then((response) => {
                    if (response.data.requests) {
                        this.requests = response.data.requests;
                        this.issuedBooks = response.data.issued;
                    } else {
                        console.error("No request data found in the response", response.data);
                        this.requests = [];
                        this.issuedBooks = [];
                    }
                })
                .catch((error) => {
                    console.error("There was an error fetching the requests!", error);
                    if (error.response && error.response.data) {
                        console.error("Error response data:", error.response.data);
                    }
                });
        },
        approveRequest(requestId) {
            const token = localStorage.getItem('accessToken');
            axios.post(`/libraryregister/approvebook/${requestId}`, { requestId }, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then((response) => {
                     // Refresh data after approval
                    this.message = response.data.message;
                    this.fetchRequests();
                })
                .catch((error) => {
                    console.error("Failed to approve request", error);
                    if (error.response && error.response.data) {
                        console.error("Error response data:", error.response.data);
                    }
                });
        },
        rejectRequest(requestId) {
            const token = localStorage.getItem('accessToken');
            axios.delete("/requestreject", {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                data: { requestId },
                withCredentials: true,
            })
                .then((response) => {
                    this.message = response.data.message;
                    this.fetchRequests(); // Refresh data after rejection
                })
                .catch((error) => {
                    console.error("Failed to reject request", error);
                    if (error.response && error.response.data) {
                        console.error("Error response data:", error.response.data);
                    }
                });
        },
        retrieveBook(requestId) {
            const token = localStorage.getItem('accessToken');
            axios.post(`/libraryregister/retrieve/${requestId}`, { requestId }, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then((response) => { // Refresh data after retrieval
                    this.message = response.data.message;
                    this.fetchRequests();
                })
                .catch((error) => {
                    console.error("Failed to retrieve book", error);
                    if (error.response && error.response.data) {
                        console.error("Error response data:", error.response.data);
                    }
                });
        }
    },
    created() {
        this.fetchRequests();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
.requests-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.requests-table th, .requests-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

.requests-table th {
    background-color: #f2f2f2;
    color: black;
}

.book-button {
    margin-right: 5px;
}
</style>
