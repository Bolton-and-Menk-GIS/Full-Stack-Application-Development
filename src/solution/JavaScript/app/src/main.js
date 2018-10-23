import Vue from 'vue'
import App from './App.vue'
import axios from 'axios';
import router from './modules/router';
import { request } from "./modules/xhr";
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import '@fortawesome/fontawesome-free/js/all';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Spinner from './components/UI/Spinner';
import Vuelidate from 'vuelidate';
import { EventBus } from './modules/EventBus';

// use Bootstrap-Vue and Vuelidate
Vue.use(BootstrapVue);
Vue.use(Vuelidate);

// register these components globally
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('spinner', Spinner);

// set $http property for typeahead component
Vue.prototype.$http = axios;

Vue.config.productionTip = false;

// wait for config to load before initializing Vue instance
request('./config.json').then((config) => {

  // set base url for API from config file
  axios.defaults.baseURL = config.api_base;

  new Vue({
    render: h => h(App),

    // register router with vue
    router,

    // mounted event
    mounted(){
      console.log('MOUNTED MAIN VUE INSTANCE');

      // listen for user login/logout events
      EventBus.$on('user-logged-in', ()=>{
        this.userIsAuthenticated = true;
        console.log('user logged in main.js')
        // this.$refs.mapView.createAddBreweryButton();
      });

      EventBus.$on('user-logged-out', ()=>{
        this.userIsAuthenticated = false;
      });
    },

    // data must be a function that returns an object
    data(){
      return {
        config: config,
        userIsAuthenticated: false
      }
    }
  }).$mount('#app');

});
