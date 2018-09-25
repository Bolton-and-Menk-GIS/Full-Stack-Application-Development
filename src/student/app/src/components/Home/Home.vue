<template>
  <div class="home-page">

    <!-- MAP VIEW-->
    <map-view ref="mapView" />

  </div>
</template>

<script>
  import MapView from './MapViewMglv';

  export default {
    name: "home",
    components: {
      MapView
    },

    data(){
      return {}
    },
    mounted(){
      console.log('MOUNTED HOME COMPONENT!');
      console.log('ref to map view: ', this.$refs.mapView);
    },

    methods: {}
  }
</script>