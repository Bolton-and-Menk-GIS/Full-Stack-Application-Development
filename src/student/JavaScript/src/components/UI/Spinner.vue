<template>
  <div class="login-spinner" v-if="visible">
    <h4>{{ text }}</h4>
    <span style="font-size: 2.5rem;" class="fas fa-spinner fa-spin mt-4"></span>
  </div>
</template>

<script>
  export default {
    name: "spinner",
    props: {
      text: {
        type: String,
        default: 'Loading...'
      },
      visible: {
        type: Boolean,
        default: true
      }
    },
    data() {
      return {}
    },
    methods: {}
  }
</script>

<style>
  .login-spinner {
    color: gray;
  }

</style>