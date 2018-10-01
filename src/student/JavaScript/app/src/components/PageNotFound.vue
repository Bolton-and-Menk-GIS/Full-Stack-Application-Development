<template>
  <div class="page-not-found centered">
    <h1>Page Not Found</h1>
    <p>Sorry, but the page you were trying to view does not exist.</p>
  </div>
</template>

<script>
  export default {
    name: "page-not-found",
    data() {
      return {}
    },
    methods: {}
  }
</script>

<style>
  .page-not-found {
    vertical-align: middle;
    margin: 2em auto;
  }
  .page-not-found > h1 {
    color: #555;
    font-size: 2em;
    font-weight: 400;
  }

  .page-not-found > p {
    margin: 0 auto;
    width: 280px;
  }

</style>