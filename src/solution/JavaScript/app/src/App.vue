<template>
  <!-- Vue instance attaches here-->
  <div id="app">

    <!-- App Navbar -->
    <app-nav-bar />

    <!-- ROUTER VIEW, ALL COMPONENTS VIEWED THROUGH ROUTER ARE DISPLAYED IN THE <router-view> -->
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  
  </div>
</template>

<script>
  import AppNavBar from './components/AppNavBar';

  export default {
    name: 'app',
    components: {
      AppNavBar
    }
  }
</script>

<style>

  /* this will serve as our global css */
  .centered {
    color: gray;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .capitalize {
    text-transform: capitalize !important;
  }

  .theme {
    color: forestgreen;
    font-weight: bold;
  }

  .theme-banner {
    background-color: forestgreen;
    /*font-weight: bold;*/
    color: white; 
  }

  .bold {
    font-weight: bold !important;
  }

  button.theme {
    min-width: 6rem;
    background-color: orange;
    border-color: orange;
    font-weight: bold;
    color: white;
  }
  button.theme:hover:enabled, button.theme.active:enabled {
    background-color: darkorange !important;
    border-color: darkorange !important;
    font-weight: bold;
    color: white;
  }

  button.theme:disabled{
    background-color: rgba(153, 61, 0, 0.3);
    cursor: not-allowed;
    color: gray;
  }


  .btn-danger {
    min-width: 6rem;
  }

  .control-btn-active {
    background-color: orange;
  }

  .control-btn-active > button {
    color: white !important;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

</style>
