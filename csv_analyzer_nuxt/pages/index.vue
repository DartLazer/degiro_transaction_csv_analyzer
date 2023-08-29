<template>
  <div>
    <div class="container mt-5">
      <transition name="fade" mode="out-in">
        <div v-if="showFileUpload" class="row">
          <h2>Analyze your degiro portfolio</h2>
          <div class="col-10 lead">
            <p>
              This tool allows you to provide a more detailed report about your stocks / ETF performance than the
              default
              degiro overview.
            </p>
            <p>
              The tool analyzes all your transactions, and queries yahoo finance for the stock prices at certain times.
              It
              then calculates
              all the statistics.
              The files you upload are <strong>not</strong> stored in any way. They are processed and discarded straight
              away. <br/><span class="small"><a href=""
                                                class="link-secondary">You can check this for yourself in our source code</a></span>
            </p>
          </div>
          <p>
            Please upload your CSV file here.
          </p>
          <h2 style="color: red;" v-if="errorMessage">{{ errorMessage }}</h2>
          <NuxtLink class="small link-secondary" to="/instructions">Click here to see the instructions on how to get the
            csv
            file
          </NuxtLink>
          <div class="col-md-12">
            <input type="file" @change="handleFileSelect" accept=".csv" class="form-control mb-3"/>
            <button @click="uploadCsvFile" class="btn btn-primary mb-5">Upload File</button>
          </div>
          <disclaimer/>
        </div>
      </transition>

      <transition name="fade" mode="out-in">
        <loading-spinner :is-loading="isLoading"/>
      </transition>

      <transition name="fade" mode="out-in">
        <port-folio-dashboard class="transition" v-if="serverResponse" :stock-data="serverResponse"/>
      </transition>
    </div>
  </div>

</template>

<script setup>
import axios from 'axios'
import Disclaimer from "~/components/disclaimer.vue";


const selectedFile = ref(null)
const serverResponse = ref(null)
const isLoading = ref(false)
const showFileUpload = ref(true)
const errorMessage = ref(null)
const handleFileSelect = (event) => {
  selectedFile.value = event.target.files[0]
}

const uploadCsvFile = async () => {
  if (!selectedFile.value) return
  let stillLoading = true
  setTimeout(() => {
    if (stillLoading) {
      console.log(stillLoading)
      isLoading.value = true
    }
  }, 700)

  showFileUpload.value = false

  const formData = new FormData()
  formData.append('csv_file', selectedFile.value, selectedFile.value.name)

  try {
    const response = await axios.post('http://localhost:8000/calculate_multi_year_gain/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    serverResponse.value = response.data
    stillLoading = false
    console.log('Server Response:', response.data)
  } catch (error) {
    console.log('Error uploading file:', error)
    errorMessage.value = "Error connecting to server"
    stillLoading = false
    showFileUpload.value = true
    isLoading.value = false
  } finally {
    isLoading.value = false
    if (!errorMessage) {
      showFileUpload.value = false
    }
  }
}
</script>

<style scoped>

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-enter-from, .fade-leave-to /* .fade-leave-active in <2.1.8 */
{
  opacity: 0;
}

</style>