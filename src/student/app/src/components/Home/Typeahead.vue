<template>
  <div class="Typeahead mt-3">
    <i class="fa fa-spinner fa-spin input-icon" v-show="loading"></i>
    <div>
      <span v-show="isEmpty"><i class="fa fa-search input-icon"></i></span>
      <span v-show="isDirty" @click="reset"><i class="fa fa-times input-icon"></i></span>
    </div>

    <b-form-input type="text"
           class="typeahead-input mt-2 ml-2"
           placeholder="Search for brewery"
           autocomplete="off"
           ref="input"
           v-model="query"
           @keydown.down="down"
           @keydown.up="up"
           @keydown.enter="hit"
           @keydown.esc="reset"
           @blur="reset"
           @input="update"/>

    <b-list-group v-show="hasItems" class="mt-1 search-results">
      <b-list-group-item v-for="(item, $item) in items" :key="item.id"
        :class="activeClass($item)"
        @mousedown="hit"
        @mousemove="setActive($item)">
          <p class="brewery-name hit-result mb-2">{{ item.name }}</p>
          <p class="hit-result mb-1">{{ item.city }}, {{ item.state }}</p>
      </b-list-group-item>

    </b-list-group>
  </div>
</template>

<script>
  import { EventBus } from "../../modules/EventBus";
  import VueTypeahead from 'vue-typeahead';

  export default {
    mixins: [VueTypeahead],
    data () {
      return {
        data: {
          wildcards: 'name'

        },
        queryParamName: 'name',
        limit: 10,
        minChars: 2
      }
    },
    mounted(){
      // focus on input
      this.$nextTick(() => this.$refs.input.focus());
    },

    computed: {
        src(){
          return `${this.$root.config.api_base}/breweries`
        }
    },

    methods: {
      onHit (item) {
        console.log('onHit: ', item);
        EventBus.$emit('brewery-search-result', {
          type: 'Feature',
          properties: item,
          geometry: {
            coordinates: [
              item.x,
              item.y]
          }
        });
      }
    }
  }
</script>

<style scoped>
  .Typeahead {
    position: relative;
  }

  .typeahead-input {
    width: 95%;
    font-size: 14px;
    text-align: center;
    /*color: #2c3e50;*/
    color: black !important;
    line-height: 1.42857143;
    box-shadow: inset 0 1px 4px rgba(0,0,0,.4);
    -webkit-transition: border-color ease-in-out .15s,-webkit-box-shadow ease-in-out .15s;
    transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s;
    font-weight: 300;
    padding: 12px 26px;
    border: none;
    border-radius: 22px;
    letter-spacing: 1px;
    box-sizing: border-box;
  }

  .hit-result {
    color: black;
  }

  .search-results > div.list-group-item {
    cursor: pointer;
  }

  .brewery-name {
    font-weight: bold;
  }

  .typeahead-input:focus {
    border-color: #4fc08d;
    outline: 0;
    box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px #4fc08d;
  }

  .input-icon{
    cursor: pointer;
    position: absolute;
    top: 0.75rem;
    right: 1.5rem;
    color: lightgray;
  }

  .active {
    background-color: #3aa373 !important;
  }

  .active > p {
    color: white;
  }

  .name {
    font-weight: 700;
    font-size: 18px;
  }

  .screen-name {
    font-style: italic;
  }
</style>