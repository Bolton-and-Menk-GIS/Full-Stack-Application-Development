import { request } from './xhr';
import axios from 'axios';

const api = {

  getBreweries({id=null, options={}}={}){
    // defaults
    options.f = options.f || 'geojson';

    // make request
    return request(`/breweries${id ? '/' + id: ''}`, options);
  },

  getBeersFromBrewery(breweryId, options={}){
    return request(`/breweries/${breweryId}/beers`, options);
  },

  getBeerPhotos(beerId, options={}){
    return request(`/beers/${beerId}/photos`, options);
  },

  getPhotoUrl(photo_id, cacheBust=true){
    // need to full url since this will likely be used in an <img> tag
    return `${axios.defaults.baseURL}/beer/photos/${photo_id}/download${cacheBust ? '?cb=' + new Date().getTime(): ''}`;
  },

  async login(usr, pw, remember_me=false){
    
    const resp = await request('/users/login', {
      method: 'post',
      username: usr,
      password: btoa(pw),
      remember: remember_me
    });
    if ('token' in resp){
      api.token = resp.token;
      axios.defaults.headers.common.Authorization = resp.token;
      console.log('LOGIN RESPONSE: ', resp);
    }
    return resp;
  },

  async logout(){
    const response = await request('/users/logout', {method: 'post'}, false);
    console.log('FULL LOGOUT RESPONSE: ', response);
    return response.data;
  },

  async fetchUsernames(){
    const resp = await request('/users?fields=username');`create`
    return resp.map(u => u.username);
  },

  async userIsActive(id){
    const resp = await request(`/users/${id}?fields=username,activated,id`);
    return resp.activated === 'True'; // stored as string in db
  },

  createUser({name, email, username, password, activation_url=default_activation_url } = {}){
    return request('/users/create', {
      method: 'post',
      data: {
        name: name,
        email: email,
        username: username,
        password: btoa(password),
        activation_url: activation_url
      }
    });

  },

  activate(id){
    return request(`/users/${id}/activate`, { method: 'post' });
  },

  authTest(){
    return request('/users/welcome');
  },

  async exportData({table='breweries', format='csv'}={}){
    try {
      return await request(`/data/${table}/export?f=${format}`, {
        method: 'post'
      });
    } catch(err){
      console.warn('export data failed: ', err);
    }
  },


}

export default api;