import Router from 'vue-router';
import Vue from 'vue';
import Home from '../components/Home/Home';
import PageNotFound from '../components/PageNotFound';
import SignUp from '../components/SignUp/SignUp';
import ActivationPage from '../components/SignUp/ActivationPage';
import EditableBreweryInfo from '../components/Editing/EditableBreweryInfo';
import EditableBeerInfo from '../components/Editing/EditableBeerInfo';

Vue.use(Router);

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/sign-up', name: 'signup', component: SignUp },
  { path: '/users/:id/activate', name: 'activate', component: ActivationPage },
  { path: '/brewery/:brewery_id', name: 'editableBreweryInfo', component: EditableBreweryInfo },
  { path: '/beers/:beer_id', name: 'editableBeerInfo', component: EditableBeerInfo },
  
  // catch all route
  { path: '*', component: PageNotFound }
];

export default new Router({
  mode: 'history',
  routes: routes
});