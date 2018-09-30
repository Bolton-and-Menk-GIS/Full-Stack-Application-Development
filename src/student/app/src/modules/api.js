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

  getDirectionsUrl(feature){
    const addr_parts = [feature.name, feature.address, feature.city, feature.state, feature.zip];

    // form query url for google directions, try address first if has address city st zip else use x,y
    const dest = addr_parts.every(f => !!f) ? addr_parts.join(' ').replace(/\s/g, '+'): `${feature.y},${feature.x}`;
    return `https://www.google.com/maps/dir/Current+Location/${dest}`;
  }

}

export default api;