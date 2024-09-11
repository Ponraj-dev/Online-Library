<!-- eslint-disable prettier/prettier -->
<template>
    <div class="userGrowth">
            <canvas id="userGrowthChart">
                </canvas>

    </div>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
    data() {
        return {
            userGrowthData: [],
        };
    },
    mounted() {
        this.fetchUserGrowthData();
    },
    methods: {
        fetchUserGrowthData() {
            const token = localStorage.getItem('accessToken');
            axios
                .get('/user_growth', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true,
                })
                .then((response) => {
                    this.userGrowthData = response.data;
                    this.createUserGrowthChart();
                })
                .catch((error) => {
                    console.error('Error fetching user growth data:', error);
                });
        },
        createUserGrowthChart() {
            const ctx = document.getElementById('userGrowthChart');
            const labels = this.userGrowthData.map((item) => item.day);
            const counts = this.userGrowthData.map((item) => item.count);

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Number of Users',
                            data: counts,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1,
                            fill: false,
                        },
                    ],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                            font: {
                                weight: 'bold',
                                size:'px', // Make x-axis labels bold
                                color:"white"
                            },
                        },
                        },
                    },
                },
            });
        },
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
/* Add any styles for your chart container here */
.userGrowth{
    width: 100%;
    height: 100%;
    padding: 20px;
    border-radius: 15px;
    background-color: #2E236C;
    color:white
}

</style>