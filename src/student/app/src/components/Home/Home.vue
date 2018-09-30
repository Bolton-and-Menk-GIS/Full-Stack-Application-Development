<template>
  <div class="home-page">

    <!-- sidebar -->
    <sidebar ref="sidebar" @toggled="handleExpand">

      <!-- slot for sidebar content -->
      <!-- TYPEAHEAD WILL GO HERE -->

      <keep-alive>

        <!-- BREWERY IDENTIFY CONTENT -->
        <brewery-info
                v-if="identifyActive"
                :userIsAuthenticated="userIsAuthenticated"
                :feature="selectedBrewery">
        </brewery-info>

      </keep-alive>

    </sidebar>

    <!-- MAP VIEW-->
    <map-view ref="mapView" 
      @brewery-identified="showBreweryInfo"
      @toggle-identify="identifyActivePanel"
      @toggle-menu="menuActivePanel"/>

    
  </div>
</template>

<script>
  import MapView from './MapViewMglv';
  import Sidebar from './Sidebar';
  import BreweryInfo from './BreweryInfo'

  export default {
    name: "home",
    components: {
      MapView,
      Sidebar,
      BreweryInfo
    },

    data(){
      return {
        selectedBrewery: null,
        menuActive: true,
        identifyActive: false,
        addBreweryActive: false,
        sidebarActive: false,
        newBreweryPoint: null,
        userIsAuthenticated: false
      }
    },

    mounted(){
      console.log('MOUNTED HOME COMPONENT!');
      console.log('ref to map view: ', this.$refs.mapView);
    },

    methods: {

      showBreweryInfo(brewery){
        // force panel to open with identify active
        this.selectedBrewery = brewery;
        if (brewery){
          this.$refs.sidebar.expand();
          this.menuActive = false;
          this.identifyActive = true;
        }
      },

      clearSelection(){
        this.selectedBrewery = null;
        if (this.identifyActive){
          this.$refs.sidebar.collapse();
        }
      },

       menuActivePanel(){
        // if identify is shown, toggle on menu
        this.sidebarActive = this.$refs.sidebar.active;
        if (this.identifyActive && this.$refs.sidebar.active){
          this.identifyActive = false;
          this.menuActive = true;
        } else {
          this.identifyActive = false;
          this.menuActive = true;
          this.$refs.sidebar.toggle();
        }
      },

      identifyActivePanel(){
        this.sidebarActive = this.$refs.sidebar.active;
        if (this.menuActive && this.$refs.sidebar.active){
          this.menuActive = false;
          this.identifyActive = true;
        } else {
          this.menuActive = false;
          this.identifyActive = true;
          this.$refs.sidebar.toggle();
        }
      },

      // Below methods are not what we normally do in Vue.js, things are done 
      // with vanilla js to interact with elements within the Mapboxgl canvas container
      handleExpand(expanded){
        // listen for sidebar to open and update move map's left position
        document.querySelector('#map').style.left = `${expanded ? 350: 0}px`;
        if (!expanded){
          this.clearActiveButtons();
        } else {
          this.activateButton(`.expand-${this.menuActive ? 'menu': 'identify'}`)
        }
      },

      clearActiveButtons(){
        const active = document.querySelectorAll('.control-btn-active:not(.add-brewery)');
        active.forEach(e => e.classList.remove('control-btn-active'));
      },

      activateButton(selector){
        // Normally do not have to do things like this in Vue
        this.clearActiveButtons();
        const btn = document.querySelector(selector);
        if (this.$refs.sidebar.active){
          if (!btn.classList.contains('control-btn-active')){
            btn.classList.add('control-btn-active');
          } else {
            btn.classList.remove('control-btn-active');
          }
        } else {
          // check if it is add brewery button
          if (selector === '.add-brewery'){
            console.log('it is add brewery button!')
            btn.classList.add('control-btn-active');
          }
        }
      }
    },
    
    watch: {

      menuActive(newVal){
        // handle state when panel is already open, and switched from identify to menu
        if (newVal){
          this.activateButton('.expand-menu');
        }
      },

      identifyActive(newVal){
        // handle state when panel is already open, and switched from menu to identify
        if (newVal){
          this.activateButton('.expand-identify');
        }
      }
    }
  }
</script>