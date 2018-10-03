<template>
  <b-card bg-variant="light" class="editable-beer" body-class="card-block">

    <!--  SPINNER FOR LOADING -->
    <span style="font-size: 3.5rem;" class="centered" v-if="state ==='loading'">
      <spinner :text="'loading beer info...'" :visible="true"/>
    </span>

    <!-- EDITABLE BREWERY CONTENT -->
    <b-container class="mx-auto" v-else>
      <b-row class="mt-3" align-h="center">
        <b-col>
          <div class="img-container" v-if="photoUrl && photoState !== 'missing'">
            <b-img :src="photoUrl" height="200" />
            <div class="mt-3">
              <b-button class="theme" @click="photoState = 'missing'">Update Photo</b-button>
            </div>
          </div>

          <div v-else class="file-uploader mx-auto w-50">
            <span v-if="photoState === 'uploading'">
              <b-alert  :show="1" v-if="photoState === 'error'" @dismissed="photoState = 'loaded'" variant="danger">Failed to Upload Photo</b-alert>
              <spinner :visible="photoState !== 'error'" text="Uploading Photo..."/>
            </span>

            <drop-zone @received-files="photoHandler" v-else />

          </div>
        </b-col>

      </b-row>

      <b-row class="mt-4">
        <b-col md="10" sm="12" align-h="center">
          <b-form-group label="Name:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-input v-model="beer.name" style="font-weight: bold;" />
          </b-form-group>
        </b-col>

      </b-row>

      <b-row class="mt-2" align-h="center">
        <b-col :sm="prop.cols * 2" :md="prop.cols" v-for="prop in beer_props" :key="prop.field">
          <b-form-group :label="prop.label + ':'" label-text-align="left">
            <b-form-input :type="prop.type" v-model="beer[prop.field]" />
          </b-form-group>
        </b-col>
      </b-row>

      <b-row class="mt-2">
        <b-col md="10" sm="12" align-h="center">
          <b-form-group label="Style:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-select :options="beerStyles" v-model="beer.style" />

          </b-form-group>
        </b-col>
      </b-row>

      <b-row class="mt-2">
        <b-col md="10" sm="12" align-h="center">
          <b-form-group label="Description:"
                        horizontal
                        label-text-align="right"
                        :label-cols="2">
            <b-form-textarea v-model="beer.description" :rows="6" />
          </b-form-group>
        </b-col>

      </b-row>

      <b-row class="mt-4 mb-4" align-h="center">
        <b-col md="10" sm="12">
          <spinner :visible="state === 'saving'" text="Saving Changes..."/>
          <b-alert :show="1" v-if="state === 'saveComplete'" @dismissed="state = 'loaded'" variant="success">Successfully Saved Changes</b-alert>
          <b-alert  :show="1" v-if="state === 'saveFailed'" @dismissed="state = 'loaded'" variant="danger">Failed to Save Changes</b-alert>
          <b-button class="theme" @click="saveChanges" v-if="state === 'loaded'">Save Changes</b-button>
        </b-col>
      </b-row>

    </b-container>

  </b-card>
</template>

<script>
  import api from '../../modules/api';
  import DropZone from '../UI/DropZone';
  import swal from 'sweetalert2';
  import { EventBus } from "../../modules/EventBus";

  export default {
    name: "beer-info",
    components: {
      DropZone
    },
    data(){
      return {
        state: 'loading',
        beer: {},
        copy: {},
        photoInfos: [],
        photoState: null,
        photoUrl: null,
        beerStyles: [],
        beer_props: [
          { label: 'IBU', field: 'ibu', type: 'number', cols: 2 },
          { label: 'Alcohol %', field: 'alc', type: 'number', cols: 2 },
          { label: 'Color', field: 'color', type: 'text', cols: 4 }
        ]
      }
    },

    async mounted(){
      hook.eb = this;
      console.log('mounted editable beer: ', this.$route.params);
      const styles = await api.getStyles();
      this.beerStyles.length = 0;
      this.beerStyles.push(...styles);
    },

    // we want to make sure to intercept this to force the router to update
    // the current beer
    beforeRouteEnter(to, from, next){
      console.log('BEFORE BEER ROUTE UPDATE: ', to, from, next);
      next(async (vm) => {
        await vm.update(to.params.beer_id);
        console.log('updated Beer and calling next: ', vm.beer);
        next();
        window.scrollTo(0,0);
      });

    },

    beforeRouteLeave (to, from, next){
      // called when the route that renders this component is about to
      // be navigated away from.
      // has access to `this` component instance.
      // make sure there haven't been any changes before leaving route
      if (JSON.stringify(this.beer) != JSON.stringify(this.copy)) {
        swal({
          type: 'warning',
          title: 'You have unsaved Edits',
          text: 'You are about to leave this page but have unsaved edits. Do you want to save your changes before proceeding?',
          showCancelButton: true,
          confirmButtonColor: 'forestgreen',
          cancelButtonColor: '#d33',
          cancelButtonText: "Don't Save Changes",
          confirmButtonText: 'Save Changes'
        }).then(async (choice) => {
          if (choice.value) {
            // save here before proceeding
            console.log('SAVE BEER HERE!');
            console.log(await this.saveChanges());
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
        if (!id){
          id = this.$route.params.beer_id;
        }
        this.beer = await api.getBeer(id);
        this.copy = Object.assign({}, this.beer);
        this.photoInfos.length = 0;
        const photoInfos = await api.getBeerPhotos(this.beer.id);
        console.log('photoInfos: ', photoInfos);
        this.photoInfos.push(...photoInfos);
        if (this.photoInfos.length){

          // set cacheBust param to true to capture when image is updated!
          this.photoUrl = api.getPhotoUrl(this.photoInfos[0].id, true);
          this.photoState = 'loaded';
        } else {
          this.photoUrl = null;
          this.photoState = 'missing';
        }
        console.log('loaded beer: ', this.beer);
        this.state = 'loaded';
        return this.beer;
      },

      emitBeerChange(){
        EventBus.$emit('beers-changed', {
          brewery_id: this.beer.brewery_id,
          beer_id: this.beer.id,
          type: 'update'
        });
      },

      async saveChanges(){
        console.log('clicked save changes');
       this.state = 'saving';
        try {
          const resp = await api.updateItem('beers', this.beer);

          // make sure to update copy so router guard isn't thrown
          this.copy = Object.assign({}, this.beer);
          this.emitBeerChange();
          this.state = 'saveComplete';
        } catch(err){
          console.log('err: ', err);
          this.state = 'saveFailed';
        }

      },

      async photoHandler(files){
        this.photoState = 'uploading';
        const photo = files[0];

        // photo already exists, we just need to update by passing in photoId
        // otherwise it will add a new one
        const photoId = this.photoInfos.length ? this.photoInfos[0].id: null;
        try{
          const resp = await api.uploadBeerPhoto(this.beer.id, photo, photoId);
          console.log('UPLOAD PHOTO RESP: ', resp);

          // now refresh photoInfos and update photoUrl
          const photoInfos = await api.getBeerPhotos(this.beer.id);
          console.log('photoInfos: ', photoInfos);
          this.photoInfos.length = 0;
          this.photoInfos.push(...photoInfos);

          // set cacheBust param to true to capture updated image!
          this.photoUrl = api.getPhotoUrl(this.photoInfos[0].id, true);
          this.emitBeerChange();
          this.photoState = 'loaded';
        } catch(err){
          console.warn('PHOTO UPLOAD ERROR: ', err);
          this.photoState = 'error';
        }

      }
    },

  }
</script>

<style scoped>

  .remove {
    color: red;
    font-size: 1.25rem;
    cursor: pointer;
  }

</style>