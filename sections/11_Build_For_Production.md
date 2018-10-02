## Build Application for Production

**TL;DR** - *The instructions for this section are outlined below.  If you do not want to copy and paste the code snippets, you can switch to the [solution branch](https://github.com/Bolton-and-Menk-GIS/Full-Stack-Application-Development/tree/11-build-for-production) for this section by running: `git checkout 11-build-for-production`*

At this point, our `Brewery Finder` application is complete with all the functionality we wanted to include.  Up to this point, we have only ran this app through our development environment.  But how do we build for production?  

Because we used the [`@vue/cli`](https://cli.vuejs.org/guide/) to create the application, there is an included npm script called `build` that we can use.  But first, let's explore how this application will be bundled.  Under the hood, the vue CLI uses [Webpack](https://webpack.js.org/) to bundle the application into one or more bundle files and will uglify the output.  Also, because we used [es6 JavaScript](https://medium.freecodecamp.org/write-less-do-more-with-javascript-es6-5fd4a8e50ee2), we also will need to use [`babel`](https://babeljs.io/) to transpile the code down to `es5` so that even Internet Explorer can run the app.

For this stuff to all work together, a couple things have been added to the `JavaScript/app` folder.  The first is a very small file called `babel.config.js` which contains the following:

```js
module.exports = {
  presets: [
    '@vue/app'
  ]
}
```

While this is a small amount of code, by using the [`@vue/app` preset](https://www.npmjs.com/package/@vue/babel-preset-app), we are basically allowing babel to transpile all new JavaScript features such as `async`, `await`, `spread operators`, etc.

The next important thing is the [`vue.config.js`](https://cli.vuejs.org/guide/webpack.html#simple-configuration) file:

```js
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
```

This is where the magic happens, as this is the condensed version of the webpack config, which is mostly abstracted now with the `@vue/cli`.  The first key set is the `baseUrl`, which is set to start relatively from the build folder for paths to all assests of the application.  

The next thing is that we want to hide all of our debugging console logs for the production version.  To accomplish this, we are tapping into the `uglifyOptions` and setting the `drop_console` to `true` when the `MODE_ENV` is `production` (which our build script will use this environment).  

And finally, because we are using Mapbox-gl and webpack, we will need to [shim](https://webpack.js.org/guides/shimming/) the `mapbox-gl` module to tell wepback how to bundle the modules.

And that is what is making it all work, as the `@vue/cli` is doing all the heavy lifting.  To build for production, make sure you're in the `JavaScript/app` folder in the terminal and enter:

```node
npm run build
```

This will take a minute to compile everything into a single `build` folder, which contains the entire application.  




