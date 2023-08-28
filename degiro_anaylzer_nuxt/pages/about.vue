<template>
  <div>
    <div class="container mt-5">
      <div class="row">
        <h1>About the Stock Analyzer</h1>
      </div>

      <div class="card-body pt-5">
        <p>Welcome to this Stock Analyzer. Developed by Rik Beernink of <a href="https://www.sky-t.nl" target="_blank">Sky-T</a>, this platform was created to provide a more detailed statistical overview than the default Degiro dashboard offers.</p>

        <p>This tool aims to improve upon the default dashboard's limitations, and it's open-source and free for anyone interested. Feel free to check out the source code or contribute on <a href="https://github.com/your-github-link-here" target="_blank">GitHub</a>.</p>

        <p>If you find this tool useful and wish to support its development, you can donate a coffee <a href="your-coffee-link-here" target="_blank">here</a>.</p>
        <hr />
        <disclaimer />
      </div>
    </div>
  </div>
</template>

<script setup>

import Disclaimer from "~/components/disclaimer.vue";
</script>
