<!-- eslint-disable prettier/prettier -->
<template>
    <div class="userGrowth">
        <canvas id="ratingChart"></canvas>
    </div>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
    data() {
        return {
            Ratings: [],
        };
    },
    mounted() {
        this.fetchRatings();
    },
    methods: {
        fetchRatings() {
            const token = localStorage.getItem('accessToken');
            axios.get('/average_ratings', {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                withCredentials: true,
            })
                .then(response => {
                    this.Ratings = response.data;
                    this.createChart();
                })
                .catch(error => {
                    console.error('Error fetching average ratings:', error);
                });
        },
        createChart() {
            const ctx = document.getElementById('ratingChart');
            const labels = this.Ratings.map(item => `${item.rating} Stars`);
            const data = this.Ratings.map(item => item.count);

            if (this.myChart) {
                this.myChart.destroy();
            }

            this.myChart = new Chart(ctx, {
                type: 'doughnut', // Use 'pie' for a pie chart
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Book Counts by Rating',
                        data: data,
                        backgroundColor: [
                            'rgba(255, 99, 132)',
                            'rgba(54, 162, 235)',
                            'rgba(255, 206, 86)',
                            'rgba(75, 192, 192)',
                            'rgba(153, 102, 255)',
                            'rgba(255, 159, 64)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    return `${tooltipItem.label}: ${tooltipItem.raw} books`;
                                }
                            }
                        }
                    }
                }
            });
        }
    },
}
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
.userGrowth {
    width: 100%;
    height: 100%;
    padding: 20px;
    border-radius: 15px;
    background-color: #2E236C;
    color:white
}
</style>