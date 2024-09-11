<template>
  <div id="app">
    <!-- Header -->
    <header>
      <Navbar />
    </header>

    <!-- Main Content -->
    <main>
      <!-- Main Content Area -->
      <router-view />
    </main>
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";

export default {
  components: {
    Navbar,
  },
};
</script>

<style>
body {
  position: relative;
  min-height: 100% !important;
  background-color: #17153b;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #c8acd6;
  display: flex;
  width: 100%;
  height: 100vh;
}

::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}
router-link {
  text-decoration: none;
}

/* Track */
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px grey;
  border-radius: 5px;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #411371;
  border-radius: 5px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #411371;
}
main {
  width: 100%;
  height: 100%;
  color: white;
}

/* Ensure Navbar is always visible on larger screens */
@media (min-width: 992px) {
  .navbar-collapse {
    max-height: none !important;
    overflow: visible !important;
  }
}
</style>
