<template>
  <div>
    <div class="row">
      <div class="col-md-12">
        <div class="card mb-3">
          <div class="card-header">
            <h4 class="pt-2">Portfolio Overview</h4>
          </div>
          <div class="card-body">
            <div class="padding-left-5">
              <p><strong>Total portfolio worth:</strong> € {{ stockData.summary.total_worth }}</p>
              <p><strong>Total portfolio gain:  </strong> €
                <span :style="{ color: stockData.summary.total_gain_percentage < 0 ? 'red' : 'green' }"> {{
                    stockData.summary.total_gain_percentage
                  }} % (€ {{ stockData.summary.total_gain }})</span></p>
              <p><strong>Total Invested:</strong> € {{stockData.summary.total_invested_all_stocks}}</p>
              <p><strong>Total realized gain:</strong> € {{stockData.summary.total_realized_gain}}</p>
              <p v-if="stockData.summary.total_realized_profit_loss > 0"><strong>Total realized profit:</strong> € {{stockData.summary.total_realized_profit_loss}}</p>
              <p><strong>Total Virtual Profit/Loss</strong> {{ (stockData.summary.total_worth + stockData.summary.total_realized_gain) -  stockData.summary.total_invested_all_stocks }}</p>

              <hr/>
              <LineChart
                  :labels="Object.keys(stockData.summary.yearly_worths_whole_portfolio)"
                  :data="Object.values(stockData.summary.yearly_worths_whole_portfolio)"
              />
            </div>
          </div>
        </div>
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
                <p><strong>Total Invested All Time: </strong>€ {{ stock.total_invested.toFixed(2) }}</p>
                <p><strong>Realized Gain : </strong>€ {{ stock.realized_gain }}</p>
                <p v-if="stock.realized_profit_loss > 0 || stock.stocks_in_possession === 0"><strong>Realized profit/loss </strong>€ {{ stock.realized_profit_loss.toFixed(2) }}</p>
                <hr />
                <p><strong>Currently Invested: </strong>€ {{ stock.currently_invested.toFixed(2) }}</p>
                <p><strong>Current Worth: </strong>€ {{ stock.final_worth.toFixed(2) }}</p>
                <p><strong>Stocks in Possession: </strong>{{ stock.stocks_in_possession }}</p>

                <p><strong>Virtual Profit / Loss: </strong><span :style="{ color: stock.profit_loss < 0 ? 'red' : 'green' }">
                  € {{ stock.profit_loss }}</span></p>

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