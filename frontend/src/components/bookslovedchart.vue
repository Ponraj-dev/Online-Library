<!-- eslint-disable prettier/prettier -->
<template>
    <div class="userGrowth">
        <canvas id="myChart"></canvas>
    </div>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
    data() {
        return {
            requestCounts: [],
        };
    },
    mounted() {
        this.fetchRequestCounts();
    },
    methods: {
        fetchRequestCounts() {
        const token = localStorage.getItem('accessToken');
        axios.get('/request_counts', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            withCredentials: true,
        })
        .then(response => {
            this.requestCounts = response.data;
            this.createChart();
        })
        .catch(error => {
            console.error('Error fetching request counts:', error);
        });
    },
        createChart() {
        const ctx = document.getElementById('myChart');
        const genres = this.requestCounts.map(item => item.genre);
        const counts = this.requestCounts.map(item => item.count);

        if (this.myChart) {
            this.myChart.destroy();
        }

        this.myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: genres,
                datasets: [{
                    label: 'Most Requested Books',
                    data: counts,
                    backgroundColor: [
                        'rgba(255, 99, 132)',
                        'rgba(255, 159, 64)',
                        'rgba(255, 205, 86)',
                        'rgba(75, 192, 192)',
                        'rgba(54, 162, 235)',
                        'rgba(153, 102, 255)',
                        'rgba(201, 203, 207)'
                        ],
                        borderColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)'
                        ],
                    borderWidth: 1,
                }],
            },
            options: {
                scales: {
                    x: {
                        grid: {
                            display: false, // Hide x-axis grid lines
                        },
                        ticks: {
                            font: {
                                weight: 'bold',
                                size:'px', // Make x-axis labels bold
                            },
                        },
                    },
                    y: {
                        grid: {
                            display: false, // Hide y-axis grid lines
                        },
                        ticks: {
                            beginAtZero: true,
                            font: {
                                weight: 'bold',
                              // Make y-axis labels bold
                            },
                        },
                    },
                }
            }
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