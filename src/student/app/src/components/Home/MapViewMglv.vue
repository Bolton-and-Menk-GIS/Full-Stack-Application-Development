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
            @map-click="mapClick"
            @map-init="mapInitialized"
            @map-load="mapLoaded">
    </mapbox>
  </div>
  
</template>

<script>
  import Mapbox from 'mapbox-gl-vue';
  import { createControlButton } from '../../modules/MenuButtonControl';
  import api from '../../modules/api';
  import { EventBus } from '../../modules/EventBus';

  export default {
    name: "map-view-mglv",
    components: {
      Mapbox
    },
    data() {
      return {
        map: null,
        selectionMarker: null,
        state: 'default'
      }
    },
    mounted(){
      console.log('MOUNTED MAP VIEW: ', this);

      // event handler for autocomplete typeahead from menu search
      EventBus.$on('brewery-search-result', (feature)=>{
        this.handleIdentify(feature, true);
      });
      
    },

    methods: {
      mapInitialized(map){
        console.log('map initialized: ', map);
        this.map = map;
      },

      async mapLoaded(map){
        console.log('MAP LOADED: ', map);

        // fetch brewery data from our API
        const brewerySource = await api.getBreweries();
        console.log('brewerySource: ', brewerySource);

        // add brewery data to map
        map.loadImage('./assets/beer.png', function (error, image) {
          if (error) throw error;
          map.addImage('beer', image);
          map.addLayer({
            "id": "breweries",
            "type": "symbol",
            "source": {
              "type": "geojson",
              "data": brewerySource
            },
            "layout": {
              "icon-image": "beer",
              "icon-size": 0.1,
              "text-field": "{name}",
              "text-size": 10,
              "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
              "text-offset": [0, 1.2],
              "text-anchor": "top"
            }
          });
        });

        // add control buttons
        const toggleMenu =(evt)=>{
          this.$emit('toggle-menu');
        };

        const menuButton = createControlButton({
          className: 'expand-menu',
          iconClass: 'fas fa-bars',
          onClick: toggleMenu,
          title: 'expand menu'
        });

        map.addControl(menuButton, 'top-left');
        // add identify button
        const toggleIdentify =(evt)=>{
          this.$emit('toggle-identify');
        };

        const identifyButton = createControlButton({
          className: 'expand-identify',
          iconClass: 'fas fa-info',
          onClick: toggleIdentify,
          title: 'expand identify window'
        });

        map.addControl(identifyButton, 'top-left');
        
      },

      mapClick(map, e) {
        console.log('map click: ', e);

        // find features
        const features = map.queryRenderedFeatures(e.point, {
          layers: ['breweries']
        });

        console.log('found features: ', features);
        if (features.length) {
          // handle selection on map
          const feature = features[0];
          this.handleIdentify(feature);
        } else if (this.selectionMarker) {
          // clear selection on map and close identify
          this.selectionMarker.remove();
          this.selectionMarker = null;
          this.$emit('cleared-selection')
        }

      },

      handleIdentify(feature, updateCenter=false){
        if (!feature){
          return;
        }
        this.$emit('brewery-identified', feature);

        // add marker to map
        if (!this.selectionMarker){

          this.selectionMarker = new mapboxgl.Marker({color: 'red'})
              .setLngLat(feature.geometry.coordinates)
              .addTo(this.map);
        } else {
          this.selectionMarker.setLngLat(feature.geometry.coordinates)//[feature.properties.x, feature.properties.y]
        }

        if (updateCenter){
          this.map.setCenter(feature.geometry.coordinates);
        }
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