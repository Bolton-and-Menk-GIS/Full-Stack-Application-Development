import Router from 'vue-router';
import Vue from 'vue';
import Home from '../components/Home/Home';
import PageNotFound from '../components/PageNotFound';

Vue.use(Router);

const routes = [
  { path: '/', name: 'home', component: Home },
  
  // catch all route
  { path: '*', component: PageNotFound }
];

export default new Router({
  mode: 'history',
  routes: routes
});