<template>
  <div class="brewery-info-container">

    <div>
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
      
    },
    computed: {
      properties(){
        return (this.feature || {}).properties || this.feature || {};
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