import axios from 'axios';

const reserved = 'url method baseUrl transformRequest transformResponse headers params paramsSerializer data timeout adapter withCredentials auth responseType responseEncoding xsrfCookieName xsrfHeaderName onUploadProgress onDownloadProgress maxContentLength validateStatus proxy maxRedirects socketPath httpAgent httpsAgent cancelToken'.split(' ');

const default_options = {
  method: 'get'
};

/**
 * Base request function built on axios.
 *
 * @description Perform basic xhr methods (get, post, etc.) to handle requests.
 *
 * since    1.0.0
 *
 * @function
 * @name request
 * @param {(string|object)} url The url for request or object containing url and options.
 * @param {object} options The options for xhr request.
 *
 * @return {Promise} The promise for xhr request
 *
 */
export async function request(url, options={}, dataOnly=true){

  // allow user to pass in url and then options, or options as the first arg
  if (typeof url === 'string'){
    options = options || {};
    options.url = url;
  } else if (typeof url === 'object'){
    options = url;
  }

  // mixin defaults
  if (!('method' in options)){
    options.method = default_options.method;
  }

  for (let key in default_options){
    if (!(key in options)) {
      if (reserved.indexOf(key) > -1) {
        options[key] = default_options[key];
      }
    }
  }

  // add params or data if necessary
  const queryOptName = options.method === 'post' ? 'data': 'params';
  const otherKeys =  Object.keys(options).filter(k => reserved.indexOf(k) < 0);
  if (!(queryOptName in options) && otherKeys.length){
    options[queryOptName] = options[queryOptName] || {};

    for (let key of otherKeys){
      options[queryOptName][key] = options[key];
      delete options[key];
    }
  }

  const response = await axios(options);
  if (dataOnly){
    return response.data;
  }
  return response;
}