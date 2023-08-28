<template>
  <div class="chart-container">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup>
import ChartJS from 'chart.js/auto';
const {labels, data} = defineProps(['labels', 'data'])


const chartRef = ref(null);
let myChart = null;

const chartData = {
  labels: labels,
  datasets: [
    {
      label: 'Total Worth per year',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
      data: data,
      fill: 'origin',
    },
  ],
};

onMounted(() => {
  myChart = new ChartJS(chartRef.value.getContext('2d'), {
    type: 'line',
    data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
});

watch(() => labels, (newVal) => {
  if (myChart) {
    myChart.data.labels = newVal;
    myChart.update();
  }
});

watch(() => data, (newVal) => {
  if (myChart) {
    myChart.data.datasets[0].data = newVal;
    myChart.update();
  }
});

</script>

<style scoped>
.chart-container {
  height: 400px; /* Adjust this value as needed */
  max-width: 100%;
  margin: 0 auto;
}
</style>
