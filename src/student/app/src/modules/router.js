import Router from 'vue-router';
import Vue from 'vue';
import Home from '../components/Home/Home';
import PageNotFound from '../components/PageNotFound';
import SignUp from '../components/SignUp/SignUp';
import ActivationPage from '../components/SignUp/ActivationPage';

Vue.use(Router);

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/sign-up', name: 'signup', component: SignUp },
  { path: '/users/:id/activate', name: 'activate', component: ActivationPage },
  
  // catch all route
  { path: '*', component: PageNotFound }
];

export default new Router({
  mode: 'history',
  routes: routes
});