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
    if (!breweryId){
      return Promise.resolve([]);
    }
    return request(`/breweries/${breweryId}/beers`, options);
  },

  getBeerPhotos(beerId, options={}){
    return request(`/beers/${beerId}/photos`, options);
  },

  getPhotoUrl(photo_id, cacheBust=true){
    // need to full url since this will likely be used in an <img> tag
    return `${axios.defaults.baseURL}/beer/photos/${photo_id}/download${cacheBust ? '?cb=' + new Date().getTime(): ''}`;
  },

}

export default api;