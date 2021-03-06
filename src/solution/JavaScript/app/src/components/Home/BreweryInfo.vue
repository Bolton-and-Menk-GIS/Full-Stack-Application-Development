<template>
  <div class="brewery-info-container">
    <b-card v-if="Object.keys(feature || {}).length">
      <span class="brewery-info-header">
        <h4><strong>{{ properties.name }}</strong></h4>
        <span class="float-right edit-btn"
              title="edit brewery info"
              @click="editBrewery"
              v-show="userIsAuthenticated" >
          <font-awesome-icon prefix="fas" icon="pen" />
        </span>
      </span>

      <hr>
      <p>{{ properties.address }}</p>
      <p>{{ properties.city }}, {{ properties.state }} {{ properties.zip }}</p>
      <b-link :href="properties.website" target="_blank" v-if="properties.website">website</b-link> | 
      <b-link :href="directionsUrl" target="_blank" v-if="directionsUrl">directions</b-link>

      <!-- featured beers -->
      <div v-if="featuredBeers.length">
        <hr>
        <h5><strong>Featured Beers</strong></h5>
        <b-list-group class="featured-beers-container">
          <b-list-group-item v-for="beer in featuredBeers" :key="beer.id">
            <featured-beer :beer="beer"></featured-beer>
          </b-list-group-item>
        </b-list-group>
      </div>

    </b-card>

    <div v-else>
      <h4 class="no-features mt-4">No Features Found</h4>
    </div>

  </div>
</template>

<script>
  import { EventBus } from "../../modules/EventBus";
  import api from '../../modules/api';
  import FeaturedBeer from './FeaturedBeer';

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
    components: {
      FeaturedBeer
    },
    data() {
      return {
        featuredBeers: []
      }
    },

    mounted(){
      console.log('MOUNTED BREWERY INFO COMPONENT: ', this);

      // load the beers
      this.fetchBeers()

      // notify this component to reload featured beers
      EventBus.$on('beers-changed', (obj)=>{
        console.log('beers-changed event received: ', obj);
        if (obj.brewery_id == this.properties.id){
          this.fetchBeers();
        }
      });
      
    },

    methods: {

      getDirectionsUrl(feature){
        const addr_parts = [feature.name, feature.address, feature.city, feature.state, feature.zip];

        // form query url for google directions, try address first if has address city st zip else use x,y
        const dest = addr_parts.every(f => !!f) ? addr_parts.join(' ').replace(/\s/g, '+'): `${feature.y},${feature.x}`;
        return `https://www.google.com/maps/dir/Current+Location/${dest}`;
      },

      editBrewery(){
        // this.$router.push(`/brewery/${this.feature.properties.id}`);
        this.$router.push({
          name: 'editableBreweryInfo',
          params: {
            brewery_id: this.feature.properties.id
          }
        });
      },

      async fetchBeers(id){
        const beers = await api.getBeersFromBrewery(id || this.properties.id);
        this.featuredBeers.length = 0;
        this.featuredBeers.push(...beers);
      }

    },

    computed: {
      properties(){
        return (this.feature || {}).properties || this.feature || {};
      },

      directionsUrl(){
        return Object.keys(this.properties).length ? this.getDirectionsUrl(this.properties): null;
      }
    },

    watch: {
      'properties.id'(newVal){
        // make sure to fetch beers each time a new brewery is identified
        this.featuredBeers = [];
        if (newVal){
          this.fetchBeers(newVal);
        }
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