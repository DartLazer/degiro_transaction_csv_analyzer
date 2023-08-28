<template>
  <div>
    <!-- Spinner and Loading text -->
    <div class="row" v-if="isLoading">
      <div class="col-md-12 text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p>Loading the stock data, please wait...</p>
      </div>
    </div>
  </div>

</template>

<script setup>
const props = defineProps({
  isLoading: {
    type: Boolean,
    required: true,
  },
});
</script>