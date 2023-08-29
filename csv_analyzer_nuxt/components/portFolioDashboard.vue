<template>
  <div>
    <div class="row">
      <div class="col-md-12">
        <h2 class="padding-left-5 pb-3">Portfolio overview</h2>
        <h5 class="padding-left-5"> Total portfolio worth: {{ stockData.summary.total_worth }}</h5>
        <h5 class="padding-left-5">
          Total portfolio gain:
          <span
              :style="{ color: stockData.summary.total_gain_percentage < 0 ? 'red' : 'green' }">
          {{ stockData.summary.total_gain_percentage }} % (€ {{ stockData.summary.total_gain }})
        </span>
        </h5>
        <div v-for="stock in stockData.results" :key="stock.stock_name">
          <div class="card mb-3">
            <div class="card-header">
              <h4 class="pt-2">{{ stock.stock_name }}</h4>
            </div>
            <div class="card-body">
              <div class="padding-left-5">
                <p><strong>Total Gain: </strong>
                  <span :style="{ color: stock.total_gain_percent < 0 ? 'red' : 'green' }">
                  {{ stock.total_gain_percent.toFixed(1) }} % (€ {{ stock.total_gain_value.toFixed(2) }})
                </span>
                </p>
              </div>
              <hr/>
              <div class="padding-left-5">
                <p><strong>Total Invested: </strong>€ {{ stock.total_invested.toFixed(2) }}</p>
                <p><strong>Current Worth: </strong>€ {{ stock.final_worth.toFixed(2) }}</p>
                <p><strong>Stocks in Possession: </strong>{{ stock.stocks_in_possession }}</p>
              </div>
              <hr/>

              <h5 class="padding-left-5">Yearly Performance</h5>
              <ul>
                <li v-for="(yearData, year) in stock.yearly_gains" :key="year">
                  <p class="mt-3">{{ year }} - <span
                      :style="{ color: yearData.virtual_gain_percentage < 0 ? 'red' : 'green' }">
                  {{ yearData.virtual_gain_percentage.toFixed(1) }}% (€{{ yearData.virtual_gain_value.toFixed(2) }})
                </span></p>
                </li>
              </ul>
              <hr/>
              <LineChart
                  :labels="Object.keys(stock.yearly_worth)"
                  :data="Object.values(stock.yearly_worth)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import LineChart from "~/components/LineChart.vue";

const props = defineProps({
  stockData: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.padding-left-5 {
  padding-left: 5px;
}
</style>