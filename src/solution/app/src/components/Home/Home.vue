<template>
  <div class="home-page">

    <!-- sidebar -->
    <sidebar ref="sidebar"
             @toggled="handleExpand">

      <!-- slot for sidebar content -->
      <typeahead v-if="menuActive" />

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
    <map-view
            ref="mapView"
            :userIsAuthenticated="userIsAuthenticated"
            @clicked-add-brewery="handleAddBrewery"
            @new-brewery-point="createNewBrewery"
            @add-brewery-cancelled="deactivateAddBrewery"
            @toggle-identify="identifyActivePanel"
            @cleared-selection="clearSelection"
            @brewery-identified="showBreweryInfo"
            @toggle-menu="menuActivePanel">
    </map-view>

  </div>
</template>

<script>
  import MapView from './MapViewMglv';
  import Sidebar from './Sidebar';
  import BreweryInfo from './BreweryInfo';
  import Typeahead from './Typeahead';
  import api from '../../modules/api';
  import { EventBus } from "../../modules/EventBus";
  import swal from 'sweetalert2';

  export default {
    name: "home",
    components: {
      MapView,
      Sidebar,
      BreweryInfo,
      Typeahead
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
      hook.home = this;

      // need to manually update this, because feature returned from map click is not
      // the original object
      EventBus.$on('brewery-changed', async (obj)=>{

        if (this.selectedBrewery && obj.id === this.selectedBrewery.properties.id){
          if (obj.type === 'delete'){
            this.clearSelection();
          } else {
            const resp = await api.getBrewery(obj.id, { f: 'geojson' });
            if (resp.features.length){
              // update brewery
              Object.assign(this.selectedBrewery, resp.features[0]);
            }
          }
        }
        if (obj.type === 'create'){
          this.deactivateAddBrewery();
        }
      });

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

      handleExpand(expanded){
        // console.log('sidebar toggled: ', expanded);
        // listen for sidebar to open and update move map's left position
        document.querySelector('#map').style.left = `${expanded ? 350: 0}px`;
        if (!expanded){
          this.clearActiveButtons();
        } else {
          // this.deactivateAddBrewery();
          this.activateButton(`.expand-${this.menuActive ? 'menu': 'identify'}`)
        }

      },

      handleAddBrewery(){
        this.addBreweryActive = true;
        this.activateButton('.add-brewery');
      },

      deactivateAddBrewery(){
        const btn = document.querySelector('.add-brewery');
        btn ? btn.classList.remove('control-btn-active'): null;
        this.addBreweryActive = false;
        this.$refs.mapView.deactivateAddBrewery();
      },


      async createNewBrewery(point){

        swal({
          title: 'Create New Brewery',
          input: 'text',
          showCancelButton: true,
          confirmButtonText: 'Create',
          confirmButtonColor: 'forestgreen',
          showLoaderOnConfirm: true,
          allowOutsideClick: ()=> !swal.isLoading(),
          preConfirm: async (name)=> {
            const lat = point.lat;
            const lng = point.lng;

            // fetch access token from root vue instance "config" prop
            const accessToken = this.$root.config.map.accessToken;
            const params = await api.maboxReverseGeocode(lat, lng, accessToken);

            // add x,y coords
            params.x = point.lng;
            params.y = point.lat;

            // add brewery name to params and create new brewery
            params.name = name;
            const resp = await api.createItem('breweries', params);

            // notify new brewery has been created
            EventBus.$emit('brewery-change', {
              id: resp.id,
              type: 'create'
            });

            this.deactivateAddBrewery();
            return resp;
          }
        }).then((res)=> {
          const newBreweryId = res.value.id;
          this.emitBreweryChange(newBreweryId, 'create');
          swal({
            title: 'Success',
            text: 'successfully created new brewery',
            confirmButtonText: 'Go To New Brewery',
            cancelButtonText: 'Stay Here',
            showCancelButton: true
          }).then((res)=>{
            res.value ? this.goToEditBrewery(newBreweryId): null;
          });

        }).catch(err =>{
          console.log('error creating brewery: ', err);
          swal({
            type: 'error',
            title: 'Unable to Create Brewery',
            text: "please make sure you're logged in to make this change"
          })
        });

      },

      goToEditBrewery(id){

        // // small timeout to prevent race conditions
        // setTimeout(()=>{
          this.$router.push({ name: 'editableBreweryInfo', params: { brewery_id: id }})
        // }, 250)
      },

      emitBreweryChange(id, type){
        EventBus.$emit('brewery-changed', {
          id: id,
          type: type
        })
      },

      clearActiveButtons(){
        const active = document.querySelectorAll('.control-btn-active:not(.add-brewery)');
        active.forEach(e => e.classList.remove('control-btn-active'));
      },

      activateButton(selector){
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
      },

      '$root.userIsAuthenticated'(newVal){
        this.userIsAuthenticated = newVal;
      }

    }
  }
</script>

<style scoped>

</style>