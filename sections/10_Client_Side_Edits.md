## Edit Breweries in the Application

**TL;DR** - *The instructions for this section are outlined below.  If you do not want to copy and paste the code snippets, you can switch to the [solution branch](https://github.com/Bolton-and-Menk-GIS/Full-Stack-Application-Development/tree/10-client-side-edits) for this section by running: `git checkout 10-client-side-edits`*

The first thing we need to do to enable editing on the client side is add the appropriate API methods.  Open the `api.js` file inside the `modules` folder.  Add the following methods:

```js
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

    // return response
    const resp =  axios.post(`/data/beer_photos/${parseInt(photoId) > 0 ? photoId + '/update': 'add'}`,
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
  ```
  
  * `createItem` - will create a new item
  * `updateItem` - will update an existing feature
  * `deleteItem` - will delete an existing feature
  * `uploadBeerPhoto` - will add/update a beer photo based on whether or not an existing beer photo `id` is passed in
  * `mapboxReverseGeocode` - will use the Mapbox REST API to reverse geocode a point to obtain an address.  This will be used when creating new breweries as they will be created by first adding a point to the map.
  
That is all of the last API methods for the client side.  Save the changes. 

### create an Editable Brewery Component

Create a new folder called `Editing` inside the `JavaScript/app/src/components` folder.  Inside that, create a vue component called `EditableBreweryInfo.vue`.  As a reminder, the component UI will look like this when complete:


Now add the following `template` to the `EditableBreweryInfo.vue` file:

```html
<template>
  <b-card bg-variant="light" class="editable-brewery">

    <!--  SPINNER FOR LOADING -->
    <span style="font-size: 3.5rem;" class="centered" v-if="state === 'loading'">
      <spinner :text="'loading brewery info...'"/>
    </span>

    <!-- EDITABLE BREWERY CONTENT -->
    <b-container class="brewery-content" v-else>
      <b-row class="mt-2">
        <b-col sm="12">
          <b-form-group label="Name:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-input v-model="brewery.name" class="bold" />
          </b-form-group>
        </b-col>
      </b-row>

      <!-- ADDRESS -->
      <b-row md="12">
        <b-col sm="12">
          <b-form-group label="Address:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-input id="address" v-model="brewery.address"/>
          </b-form-group>
        </b-col>
      </b-row>

      <!--  city, st zip -->
      <b-row class="mt-2" align-h="end">
          <b-col sm="12" md="5">
            <b-form-group label="City:" label-text-align="left">
              <b-form-input v-model="brewery.city" />
            </b-form-group>
          </b-col>
          <b-col sm="6" md="3">
            <b-form-group label="State:" label-text-align="left">
              <b-form-select :options="stateList" v-model="brewery.state"></b-form-select>
            </b-form-group>
          </b-col>

          <b-col sm="6" md="2">
            <b-form-group label="Zip Code:" label-text-align="left">
              <b-form-input v-model="brewery.zip"/>
            </b-form-group>
          </b-col>
        <!--</div>-->
      </b-row>

      <!-- WEBSITE -->
      <b-row class="mt-2">
        <b-col sm="12">
          <b-form-group label="Website:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-input id="website" v-model="brewery.website" style="color:#0000EE;"/>
          </b-form-group>
        </b-col>
      </b-row>

      <!--  WEEKDAY HOURS -->
      <b-row class="mt-2" >
        <b-col sm="12" md="6">
          <b-form-group v-for="weekday in weekday_fields"
                        horizontal
                        :label-cols="5"
                        label-class="capitalize"
                        :label="`${weekday} Hours:`"
                        :key="weekday" class="mt-2">
            <b-form-input :id="weekday" v-model="brewery[weekday]" placeholder="ex: 11am-7pm" />
          </b-form-group>
        </b-col>
        <b-col sm="12" md="6">
          <b-form-group label="Brewery Description:" label-text-align="left" class="mt-2" id="description">
            <b-form-textarea :rows="weekday_fields.length + 6" v-model="brewery.comments"></b-form-textarea>
          </b-form-group>
        </b-col>

      </b-row>

      <!--  SAVE BUTTON AND TYPE -->
      <b-row class="mt-4">
        <b-col sm="6">
          <b-form-group label="Type">
            <b-form-radio-group v-model="brewery.brew_type" :options="typeOptions">
            </b-form-radio-group>
          </b-form-group>
        </b-col>

        <b-col sm="6">
          <div class="save-container">
            <div class="buttons-container" v-if="state === 'loaded'">
              <b-button @click="saveChanges" class="theme mt-2" >Save Changes</b-button>
              <b-button class="bold mt-2 ml-4" variant="danger" @click="deleteBrewery">Delete Brewery</b-button>
            </div>

            <div v-else>
              <spinner text="Saving Changes..." :visible="state === 'saving'"/>

              <b-alert :show="1" @dismissed="state = 'loaded'"
                       v-if="state === 'saved'"
                       variant="success">
                Successfully Updated Brewery.
              </b-alert>

              <b-alert :show="1" @dismissed="state = 'loaded'"
                       v-if="state === 'error'"
                       variant="danger">
                Failed to Update Brewery, please try again.
              </b-alert>
            </div>
          </div>
        </b-col>
      </b-row>

      <!--  BEER ROWS -->

    </b-container>

  </b-card>
</template>
```

The template when rendered will look like the following:

![editable beer](images/app_images/editable_brewery1.PNG)

There is not a whole lot of magic involved in the above template, it is mostly just standard form inputs that we will add and display using the `Bootstrap-Vue` components and the [bootstrap grid system](https://bootstrap-vue.js.org/docs/components/layout/)

```html
<script>
  import api from '../../modules/api';
  import enums from '../../modules/enums';
  import Accordion from '../UI/Accordion';
  import { EventBus } from "../../modules/EventBus";
  import swal from 'sweetalert2';

  export default {
    name: "brewery-info",
    components: {
      Accordion
    },
    data(){
      return {
        state: 'loading',
        brewery: {},
        copy: {},
        weekday_fields: ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'],
        stateList: enums.states,
        beers: [],
        typeOptions: [
          { text: 'Brewery', value: 'Brewery' },
          { text: 'Brew Pub', value: 'Brew Pub' }
        ]
      }
    },

    async mounted(){
      console.log('mounted editable brewery: ', this.$route.params);
    },

    // we want to make sure to intercept this to force the router to update
    // the current brewery
    beforeRouteEnter(to, from, next){
      next(async (vm)=>{
        // vm is reference to this component!
        await vm.update(to.params.brewery_id);
        console.log('updated brewery and calling next: ', vm.brewery);
        next();
      })

    },

    beforeRouteLeave (to, from, next) {
      // called when the route that renders this component is about to
      // be navigated away from.
      // has access to `this` component instance.
      // make sure there haven't been any changes before leaving route
      console.log('BEFORE BREWERY ROUTE LEAVE')
      if (this.state !== 'deleted' && JSON.stringify(this.brewery) != JSON.stringify(this.copy)){
        swal({
          type: 'warning',
          title: 'You have unsaved Edits',
          text: 'You are about to leave this page but have unsaved edits. Do you want to save your changes before proceeding?',
          showCancelButton: true,
          confirmButtonColor: 'forestgreen',
          cancelButtonColor: '#d33',
          cancelButtonText: "Don't Save Changes",
          confirmButtonText: 'Save Changes'
        }).then((choice)=>{
          if (choice){
            // save here before proceeding
            console.log('SAVE HERE!');
            this.saveChanges();
          }

          // now proceed
          next();
        })
      } else {
        next();
      }
    },

    methods: {
      async update(id){
        this.state = 'loading';
        this.beers.length = 0;
        if (!id){
          id = this.$route.params.brewery_id;
        }
        this.brewery = await api.getBreweries({id: id, options: { f: 'json'} });
        this.copy = Object.assign({}, this.brewery);
        this.updateBeers();
        this.state = 'loaded';
        return this.brewery;
      },

      async updateBeers(){
        this.beers.length = 0;
        this.beers.push(...await api.getBeersFromBrewery(this.brewery.id));
      },

      deleteBrewery(){
        console.log('clicked delete brewery!')
      },

      async saveChanges(){
        console.log('submitting edits: ', this.brewery);
        this.state = 'saving';
        try {
          const resp = await api.updateItem('breweries', this.brewery);

          // make sure to update copy so router guard isn't thrown
          this.copy = Object.assign({}, this.brewery);

          // emit change
          this.emitBreweryChange('update');
          this.state = 'saved';
        } catch(err){
          console.log('err: ', err);
          this.state = 'error';
        }

      },

      emitBreweryChange(type){
        EventBus.$emit('brewery-changed', {
          id: this.brewery.id,
          type: type
        });
      },
      
    }
  }
</script>
```

Save the changes.  In order to test this at the current state, we will need to register this component with the router.  Open the `modules/router.js` file and import the `EditableBreweryInfo.vue` file:

```js
import EditableBreweryInfo from '../components/Editing/EditableBreweryInfo';
```

Next, update the `routes` array to match this:

```js
const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/sign-up', name: 'signup', component: SignUp },
  { path: '/users/:id/activate', name: 'activate', component: ActivationPage },
  { path: '/brewery/:brewery_id', name: 'editableBreweryInfo', component: EditableBreweryInfo },
  
  // catch all route
  { path: '*', component: PageNotFound }
];
```

Save the changes and try navigating to the first brewery by changing the url to the following (you may have to adjust the port number):

[`http:localhost:8080/breweries/1`](http:localhost:8081/breweries/1)

For the `name`, `address`, and `website` components, the form inputs will take up the whole width ()
```html

```
 







