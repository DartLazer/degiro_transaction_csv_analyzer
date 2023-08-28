<template>
  <div class="chart-container">
    <Line :data="chartData" :options="options"/>
  </div>
</template>

<script setup>
import {Line} from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)
const {labels, data} = defineProps(['labels', 'data'])


const chartData = ref({
  labels: labels,
  datasets: [
    {
      label: 'Total Worth per year',
      backgroundColor: 'rgba(75, 192, 192, 1)',  // Background color with transparency
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
      data: data
    }
  ]
})

watch(() => labels, newVal => {
  chartData.value.labels = newVal
})

watch(() => data, newVal => {
  chartData.value.datasets[0].data = newVal
})

const options = ref({
  responsive: true,
  maintainAspectRatio: false,
})

</script>

<style scoped>
.chart-container {
  height: 400px; /* Adjust this value as needed */
  max-width: 100%;
  margin: 0 auto;
}
</style>
