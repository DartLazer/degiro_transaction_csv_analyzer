<template>
  <div class="chart-container">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup>
import ChartJS from 'chart.js/auto';

const {labels, data} = defineProps(['labels', 'data'])

const formattedLabels = labels.map(timestamp => {
  const date = new Date(timestamp * 1000);
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const year = String(date.getFullYear()).substr(-2);

  return `${month}-${day}-${year}`;
});


const chartRef = ref(null);
let myChart = null;

const chartData = {
  labels: formattedLabels,
  datasets: [
    {
      label: 'Total Worth per year',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
      cubicInterpolationMode: 'monotone',
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
