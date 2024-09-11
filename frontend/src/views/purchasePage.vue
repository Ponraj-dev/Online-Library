<!-- eslint-disable prettier/prettier -->
<template>
    <div class="mainscreen">
        <div class="card">
            <div class="leftside">
                <div v-for="ebook in ebooks" :key="ebook.id" class="image-container">
                    <img :src="getUserImage(ebook.profile_image)" alt="Book Image" class="purchase-image-book" />
                    <div class="overlay">
                        <div class="overlay-content">
                            <h3>{{ ebook.bookname }}</h3>
                            <p class="prise">$99</p>
                            <p class="stars">
                                <span v-for="star in 5" :key="star" class="fa fa-star"
                                    :class="{ 'checked': average_rating >= star }"></span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="rightside">
                <form @submit.prevent="handleSubmit">
                    <h2>Payment Information</h2>
                    <p>Cardholder Name</p>
                    <input type="text" class="inputbox" v-model="formData.name" required />
                    <p>Card Number</p>
                    <input type="number" class="inputbox" v-model="formData.card_number" required />
                    <p>Card Type</p>
                    <select class="inputbox" v-model="formData.card_type" required>
                        <option value="">--Select a Card Type--</option>
                        <option value="Visa">Visa</option>
                        <option value="RuPay">RuPay</option>
                        <option value="MasterCard">MasterCard</option>
                    </select>
                    <div class="expcvv">
                        <p class="expcvv_text">Expiry</p>
                        <input type="date" class="inputbox" v-model="formData.exp_date" required />
                        <p class="expcvv_text2">CVV</p>
                        <input type="password" class="inputbox" v-model="formData.cvv" required />
                    </div>
                    <router-link class="viewMore" to="/downloads"><button type="submit"
                            class="button">CheckOut</button></router-link>
                </form>
            </div>
        </div>
    </div>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from "axios";

export default {
    data() {
        return {
            ebooks: [],
            formData: {
                name: "",
                card_number: "",
                card_type: "",
                exp_date: "",
                cvv: "",
            },
            rating: {
                value: null,
                description: ''
            },
            ratings: [],
            average_rating: "",
        };
    },
    name: "Purchase",
    methods: {
        getUserImage(base64Image) {
            if (base64Image) {
                return `data:image/jpeg;base64,${base64Image}`;
            }
            return ""; // Optionally provide a placeholder image
        },
        handleSubmit() {
            // Handle form submission logic here
            alert("Form submitted");
        },
        fetchUsers() {
            let token = localStorage.getItem("accessToken");
            const bookId = this.$route.params.bookId || "";
            this.selectedBook = bookId;

            axios
                .get(`/purchasePage/${bookId}`, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        Authorization: `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.ebooks = response.data.ebooks;
                    this.ratings = response.data.rating;
                    this.average_rating = response.data.average_rating;
                })
                .catch((error) => {
                    console.error("There was an error fetching the book data!", error);
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
body {
    font-family: "Roboto", sans-serif !important;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.mainscreen {
    min-height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: column;
    background-image: url("https://wallpaperaccess.com/full/258527.jpg");
    color: #963e7b;
}

.card {
    width: 60rem;
    margin: auto;
    color: #ccc;
    background: #ffffff1a;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 1.5rem;
    box-shadow: 4px 3px 20px #3535358c;
    display: flex;
    flex-direction: row;
}

.leftside {
    position: relative;
    width: 25rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-top-left-radius: 1.5rem;
    border-bottom-left-radius: 1.5rem;
}

.image-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.purchase-image-book {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 1.5rem;
}

.prise {
    font-size: 4rem;
    font-weight: bold;
}

.overlay {
    position: absolute;

    left: 0;
    bottom: 0;
    width: 100%;
    height: 30%;
    background-color: #1c1a1a91;
    color: white;
    border-radius: 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: end;
    z-index: 1;
}

.overlay-content {
    text-align: center;
}

.overlay-content h3 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
}

.overlay-content p {
    margin: 0.5rem 0;
}

.stars {
    margin-top: 0.5rem;
}

.star {
    color: gold;
    font-size: 1.5rem;
}

.empty {
    color: #ccc;
}

.rightside {
    width: 35rem;
    border-bottom-right-radius: 1.5rem;
    border-top-right-radius: 1.5rem;
    padding: 1rem 2rem 3rem 3rem;
}

p {
    display: block;
    font-size: 1.1rem;
    font-weight: 400;
    margin: 0.8rem 0;
}

.inputbox {
    color: #030303;
    width: 100%;
    padding: 0.5rem;
    border: none;
    border-bottom: 1.5px solid #ccc;
    margin-bottom: 1rem;
    border-radius: 0.3rem;
    font-family: "Roboto", sans-serif;
    font-size: 1.1rem;
    font-weight: 500;
    outline: none;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff; /* White text color */
}

.expcvv {
    display: flex;
    justify-content: space-between;
    padding-top: 0.6rem;
}

.expcvv_text {
    padding-right: 1rem;
}

.expcvv_text2 {
    padding: 0 1rem;
}

.button {
    background:#c992b9;
    padding: 15px;
    border: none;
    border-radius: 50px;
    color: rgb(30, 30, 30);
    font-weight: 400;
    font-size: 1.2rem;
    margin-top: 10px;
    width: 100%;
    letter-spacing: 0.11rem;
    outline: none;
}

.button:hover {
    transform: scale(1.05) translateY(-3px);
    box-shadow: 3px 3px 6px #38373785;
}

.checked {
    color: orange;
}

.rating-form,
.rating-display {
    margin: 20px 0;
}

.rating-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}


.stars {
    display: inline-block;
}

.fa-star {
    font-size: 20px;
    cursor: pointer;
}
@media only screen and (max-width: 1000px) {
    .card {
        flex-direction: column;
        width: auto;
    }

    .leftside {
        width: 100%;
        border-top-right-radius: 0;
        border-bottom-left-radius: 0;
        border-radius: 0;
    }

    .rightside {
        width: auto;
        border-bottom-left-radius: 1.5rem;
        padding: 0.5rem 3rem 3rem 2rem;
        border-radius: 0;
    }
}
</style>