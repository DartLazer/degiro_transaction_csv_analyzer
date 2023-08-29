<template>
  <div>
    <nav class="navbar navbar-expand-lg" aria-label="Navbar"
         style="background: RGBA(248, 249, 250, 0.5)">
      <div class="container">
        <NuxtLink class="navbar-brand" to="/">
          CSV Stock Analyzer
        </NuxtLink>
        <button class="navbar-toggler collapsed" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarsExample07" aria-controls="navbarsExample07" aria-expanded="false"
                aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div ref="navbarRef" class="navbar-collapse collapse" id="navbarsExample07" style="">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <NuxtLink @click.native="collapseNavbar" class="nav-link"
                        active-class="active" to="/">Home
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink @click.native="collapseNavbar" class="nav-link" exact-active-class="active"
                        to="/about">About
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink @click.native="collapseNavbar" class="nav-link" exact-active-class="active"
                        to="/instructions">Instructions
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>

  </div>
</template>

<script setup>
const navbarRef = ref(null);

const collapseNavbar = () => {
  if (navbarRef.value) {
    navbarRef.value.className = 'navbar-collapse collapse';
  }
}
</script>