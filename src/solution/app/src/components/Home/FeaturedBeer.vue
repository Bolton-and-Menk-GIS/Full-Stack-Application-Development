<template>
  <div>
    <b-media>
      <b-img rounded blank-color="#ccc" width="200" :src="imgSrc" v-show="imgSrcLoaded" :title="beer.name"></b-img>

      <h6 class="mt-2"><strong>{{ beer.name }}</strong></h6>

      <div class="featured-beer-body">
        <p style="text-align: center;">{{ beer.description }}</p>
        <span class="beer-info">
          <p>Style: {{ beer.style }}</p>
          <p>Alc: {{ beer.alc }}% by Vol</p>
          <p>IBU: {{ beer.ibu }}</p>
          <p>Color: {{ beer.color }}</p>
        </span>

      </div>

    </b-media>
  </div>
</template>

<script>
  import api from '../../modules/api';

  export default {
    name: "featured-beer",
    props:{
      beer: {
        type: Object,
        default(){
          return {};
        }
      }
    },
    data() {
      return {
        imgSrc: null,
        imgSrcLoaded: false
      }
    },
    async beforeMount(){
      // send off request before this is mounted
      const photos = await api.getBeerPhotos(this.beer.id);
      console.log('beer photos: ', photos);
      if (photos.length){
        console.log('setting photo url: ', api.getPhotoUrl(photos[0].id));
        this.imgSrc = api.getPhotoUrl(photos[0].id)
      }
    },
    methods: {},
    watch: {
      imgSrc(newVal){
        if (newVal){
          this.imgSrcLoaded = true;
        }
      }
    }
  }
</script>

<style>
  .featured-beer-body {
    text-align: left;
  }

  .beer-info > p {
    font-size: 95%;
    margin-top: 2px !important;
    margin-bottom: 2px !important;
  }

</style>