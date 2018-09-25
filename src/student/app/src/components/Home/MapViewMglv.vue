<template>
  <div class="map-container">
    <mapbox
            :access-token="$root.config.map.accessToken"
            :map-options="{
                style: $root.config.map.mapStyle,
                center: $root.config.map.center,
                zoom: $root.config.map.zoom
            }"
            :nav-control="{
              show: true,
              position: 'top-left'
            }"
            :geolocate-control="{
                show: true,
                position: 'top-left'
            }"
            :scale-control="{
                show: true,
                position: 'bottom-right'
            }"
            @map-init="mapInitialized"
            @map-load="mapLoaded">
    </mapbox>
  </div>
  
</template>

<script>
  import Mapbox from 'mapbox-gl-vue';

  export default {
    name: "map-view-mglv",
    components: {
      Mapbox
    },
    data() {
      return {
        map: null
      }
    },
    mounted(){
      console.log('MOUNTED MAP VIEW: ', this);
    },
    methods: {
      mapInitialized(map){
        console.log('map initialized: ', map);
        this.map = map;

      },

      async mapLoaded(map){
        console.log('MAP LOADED: ', map);
      }
    }
  }
</script>

<style>
  #map {
    position: absolute;
    top: 60px;
    bottom:0;
    right: 0;
    left: 0;
  }

  /* need to override this */
  .mapboxgl-canvas{
    position: relative !important;
  }

</style>