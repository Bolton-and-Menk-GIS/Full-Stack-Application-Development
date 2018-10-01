<template>
  <b-navbar toggleable="md" type="dark" class="theme-banner app-header" :sticky="true">
    <b-navbar-brand href="#"><strong>Brewery Finder</strong></b-navbar-brand>

    <b-navbar-nav class="ml-auto">

    </b-navbar-nav>
  </b-navbar>
</template>

<script>
 
  export default {
    name: "app-nav-bar",
    data() {
      return {}
    },
    async mounted(){
      console.log('MOUNTED APP NAV BAR: ', this);
    },

    methods: {},
  }
</script>

<style scoped>

</style>