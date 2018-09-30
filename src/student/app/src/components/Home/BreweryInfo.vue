<template>
  <div class="brewery-info-container">
    <b-card v-if="Object.keys(feature || {}).length">
      <span class="brewery-info-header">
        <h4><strong>{{ properties.name }}</strong></h4>
        <span class="float-right edit-btn"
              title="edit brewery info"
              v-show="userIsAuthenticated" >
          <font-awesome-icon prefix="fas" icon="pen" />
        </span>
      </span>

      <hr>
      <p>{{ properties.address }}</p>
      <p>{{ properties.city }}, {{ properties.state }} {{ properties.zip }}</p>
      <b-link :href="properties.website" target="_blank" v-if="properties.website">website</b-link> |
      <b-link :href="directionsUrl" target="_blank" v-if="directionsUrl">directions</b-link>

      <!-- featured beers will go here -->

    </b-card>

    <div v-else>
      <h4 class="no-features mt-4">No Features Found</h4>
    </div>

  </div>
</template>

<script>
  import { EventBus } from "../../modules/EventBus";

  export default {
    name: "brewery-info",
    props: {
      feature: {
        type: Object,
        default(){
          return {
            properties: {}
          }
        }
      },
      userIsAuthenticated: false
    },

    data() {
      return {
        featuredBeers: []
      }
    },

    mounted(){
      console.log('MOUNTED BREWERY INFO COMPONENT: ', this);
      
    },

    methods: {

      getDirectionsUrl(feature){
        const addr_parts = [feature.name, feature.address, feature.city, feature.state, feature.zip];

        // form query url for google directions, try address first if has address city st zip else use x,y
        const dest = addr_parts.every(f => !!f) ? addr_parts.join(' ').replace(/\s/g, '+'): `${feature.y},${feature.x}`;
        return `https://www.google.com/maps/dir/Current+Location/${dest}`;
      },

    },

    computed: {
      properties(){
        return (this.feature || {}).properties || this.feature || {};
      },

      directionsUrl(){
        return Object.keys(this.properties).length ? this.getDirectionsUrl(this.properties): null;
      }
    }
  }
</script>

<style scoped>

  .edit-btn {
    color: forestgreen;
    font-size: 1.25rem;
    cursor: pointer;
  }

  .brewery-info-header{
    display: flex;
    justify-content: space-around;
  }

  .no-features {
    color: gray;
  }

  .featured-beers-container {
    max-height: 650px;
    overflow-y: auto;
  }

</style>