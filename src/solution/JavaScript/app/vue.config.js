const webpack = require('webpack');
module.exports = {
  baseUrl: './',
  configureWebpack: config => {
    // this is not documented very well!

    // drop console logs for production
    if (process.env.NODE_ENV === 'production') {
      if ('uglifyOptions' in config.optimization.minimizer[0].options || {}) {
        console.log('dropping console logs for production.');
        config.optimization.minimizer[0].options.uglifyOptions.compress.drop_console = true;
      }
    }

    // now we must provide a webpack plugin for mapbox-gl
    // https://github.com/phegman/vue-mapbox-gl#importing-mapbox-gl-js-with-webpack
    config.plugins.push(new webpack.ProvidePlugin({
      mapboxgl: 'mapbox-gl'
    }));
  }
};