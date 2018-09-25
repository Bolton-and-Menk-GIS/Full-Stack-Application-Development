import { request } from './xhr';
import axios from 'axios';
import enums from './enums';

const default_request_options = {
  method: 'get',
  f: 'geojson'
};

const default_activation_url = window.location.href.replace('/sign-up', '/users/{id}/activate');

const api = {
  token: null,

  getBreweries(options=default_request_options){

    // defaults
    options.method = options.method || 'get';
    options.f = options.f || 'geojson';

    // make request
    return request('/breweries', options);
  },

  getBrewery(id, options=default_request_options){
    if (id){
      return request(`/breweries/${id}`, options);
    }

  },

  getBeersFromBrewery(breweryId, options={}){
    return request(`/breweries/${breweryId}/beers`, options);
  },

  getBeer(id){
    return request(`/beers/${id}`);
  },

  getBeers(options={}){
    return request('/beers', options);
  },

  getBeerPhotos(beerId, options={}){
    return request(`/beers/${beerId}/photos`, options);
  },

  queryBeerPhotos(photo_id, options={}){
    let url = '/beer_photos';
    if (photo_id){
      url += `/${photo_id}`;
    }
    return request(url, options);
  },

  getPhotoUrl(photo_id, cacheBust=false){
    return `${axios.defaults.baseURL}/beer_photos/${photo_id}/download${cacheBust ? '?cb=' + new Date().getTime(): ''}`;
  },


  downloadPhoto(photo_id, options){
    return request(`/beer_photos/${photo_id}`, options);
  },

  async getStyles(options, asOptions=true){
    const resp = await request('/beer/styles', options);
    if (asOptions){
      return resp.map(s => s.style_name).sort().map(s => { return { text: s, value: s } });
    }
    return resp;
  },

  async login(usr, pw, remember_me=false){
    const resp = await request('/users/login', {
      method: 'post',
      username: usr,
      password: btoa(pw),
      remember: remember_me
    });
    api.token = resp.token;
    axios.defaults.headers.common.Authorization = resp.token;
    console.log('LOGIN RESPONSE: ', resp);
    return resp;
  },

  async logout(){
    const response = await request('/users/logout', {method: 'post'}, false);
    console.log('FULL LOGOUT RESPONSE: ', response);
    return response.data;
  },

  async fetchUsernames(){
    const resp = await request('/users?fields=username');
    return resp.map(u => u.username);
  },

  async userIsActive(id){
    const resp = await request(`/users/${id}?fields=username,active,id`);
    return resp.active === 'True'; // stored as string in db
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

  createItem(table, options={}){
    options.method = 'post';
    return request(`/data/${table}/create`, options);
  },

  updateItem(table, data={}){
    const options = { method: 'put', data: data };
    const id = data.id;
    return request(`/data/${table}/${id}/update`, options);
  },

  deleteItem(table, id){
    return request(`/data/${table}/${id}/delete`, { method: 'delete' });
  },

  async uploadBeerPhoto(beer_id, file, photoId=null){

    // form data will store the photo blob in request body
    const formData = new FormData();

    // add photo blob
    formData.append('photo', file, file.name);
    formData.append('beer_id', beer_id);

    // if (parseInt(photoId) > 0 ){
    //   // delete photo first, then add a new one
    //   const delResp = axios.delete(``)
    // }

    // return response
    const resp = axios.post(parseInt(photoId) > 0 ? `/beer_photos/${photoId}/update`: '/beer_photo/add',
    // const resp = axios.post('/beer_photo/add',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data' // required for form data
        }
      }
    );
    console.log('PHOTO RESP API: ', resp);
    return resp;
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

  async maboxReverseGeocode(lat, lng, access_token){
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng}%2C${lat}.json?access_token=${access_token}`;
    const resp = await request(url);
    if ((resp.features || []).length){
      const allParts = resp.features[0].place_name.split(',');

      // we only want the last 4 parts, if is an existing place in mapbox the name of place is returned first...skip this!
      const parts = allParts.splice(allParts.length - 4, allParts.length);
      const stZip = parts[2].split(' ').filter(s => s.length);
      return {
        address: parts[0],
        city: parts[1].trim(),
        state: enums.statesLookup[stZip[0]],
        zip: stZip[1]
      }
    }
    return {
      address: null,
      city: null,
      state: null,
      zip: null
    }
  }
};

export default api;