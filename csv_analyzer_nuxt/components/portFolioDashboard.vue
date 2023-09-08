<template>
  <div>
    <div class="row">
      <div class="col-md-12">

        <!-- Total Portfolio Overview Section -->
        <div class="card mb-3">
          <div class="card-header">
            <h4 class="pt-2">Portfolio Overview</h4>
          </div>
          <div class="card-body">
            <div class="padding-left-5">
              <p><strong>Total portfolio worth:</strong> € {{ stockData.summary.total_worth }}</p>
              <p><strong>Total portfolio gain: </strong> €
                <span :style="{ color: stockData.summary.total_gain_percentage < 0 ? 'red' : 'green' }"> {{
                    stockData.summary.total_gain_percentage
                  }} % (€ {{ stockData.summary.total_gain }})</span></p>
              <hr />
              <p><strong>Total all-time Invested:</strong> € {{ stockData.summary.total_invested_all_stocks }}</p>
              <p v-if="stockData.summary.total_realized_gain"><strong>Total realized gain:</strong> € {{ stockData.summary.total_realized_gain }}</p>
              <p v-if="stockData.summary.total_realized_profit_loss > 0"><strong>Total realized profit:</strong> €
                {{ stockData.summary.total_realized_profit_loss }}</p>
              <hr />
              <p><strong>Total Virtual Profit/Loss: €</strong> {{
                  ((stockData.summary.total_worth + stockData.summary.total_realized_gain) - stockData.summary.total_invested_all_stocks).toFixed(2)
                }}</p>

              <hr/>
              <LineChart
                  :labels="Object.keys(stockData.summary.yearly_worths_whole_portfolio)"
                  :data="Object.values(stockData.summary.yearly_worths_whole_portfolio)"
              />
            </div>
          </div>
        </div>

        <!-- Card per stock/etf -->
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
                <p v-if="stock.realized_profit_loss > 0 || stock.stocks_in_possession === 0"><strong>Realized
                  profit/loss </strong>
                  <span :style="{ color: stock.realized_profit_loss < 0 ? 'red' : 'green' }">
                    € {{ stock.realized_profit_loss.toFixed(2) }}
                  </span></p>

                <!--- Currently Held Section -->
                <section id="section_to_display_current_stats" v-if="stock.stocks_in_possession > 0">
                  <hr/>
                  <p><strong>Currently Invested: </strong>€ {{ stock.currently_invested.toFixed(2) }}</p>
                  <p><strong>Current Worth: </strong>€ {{ stock.final_worth.toFixed(2) }}</p>
                  <p><strong>Stocks in Possession: </strong>{{ stock.stocks_in_possession }}</p>

                  <p><strong>Virtual Profit / Loss: </strong><span
                      :style="{ color: stock.profit_loss < 0 ? 'red' : 'green' }">
                  € {{ stock.profit_loss }}</span></p>
                </section>

              </div>

              <!---- Section To Display Yearly stats -->
              <section id="Section to display yearly gains" v-if="stock.yearly_gains">
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
              </section>

              <!--- Section to display Line Chart -->
              <section v-if="!checkIfChartDataEmpty(Object.values(stock.yearly_worth))">
                <hr/>
                <LineChart
                    :labels="Object.keys(stock.yearly_worth)"
                    :data="Object.values(stock.yearly_worth)"
                />
              </section>
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

const checkIfChartDataEmpty = function (chartDataValues) {
  let allValuesZero = true;
  for (const timestampValue of chartDataValues){
    if (timestampValue !== 0){
      return false;
    }
  }
  return allValuesZero
}

</script>

<style scoped>
.padding-left-5 {
  padding-left: 5px;
}
</style>