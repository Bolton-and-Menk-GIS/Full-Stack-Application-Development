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
      <b-link :href="properties.website" target="_blank" v-if="properties.website">view website</b-link>


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
  import api from '../../modules/api';
  import FeaturedBeer from './FeaturedBeer';
  import { EventBus } from "../../modules/EventBus";

  export default {
    name: "brewery-info",
    components: {
      FeaturedBeer
    },
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
      hook.bi = this;
      this.fetchBeers();

      // notify this component to reload featured beers
      EventBus.$on('beers-changed', (obj)=>{
        if (obj.brewery_id == this.properties.id){
          this.fetchBeers();
        }
      })
    },

    methods: {

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
        if (!this.properties.id){
          return;
        }
        const beers = await api.getBeersFromBrewery(id || this.properties.id);
        this.featuredBeers.length = 0;
        this.featuredBeers.push(...beers);
      }
    },
    computed: {
      properties(){
        return (this.feature || {}).properties || this.feature || {};
      }
    },

    watch: {
      'properties.id'(newVal){
        // make sure to fetch beers each time a new brewery is identified
        this.featuredBeers.length = 0;
        this.fetchBeers(newVal);
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