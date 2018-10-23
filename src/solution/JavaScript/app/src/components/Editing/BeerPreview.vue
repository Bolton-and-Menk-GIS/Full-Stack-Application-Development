<template>
  <b-list-group-item>
    <b-media>
      <b-img-lazy slot="aside" :src="thumbnailUrl" v-if="thumbnailUrl" height="128"/>
      <span slot="aside" title="no image available" v-else><font-awesome-icon prefix="fas" icon="image" class="no-img"/></span>
      <h5>{{ beer.name }}
        <span class="float-right action-btn" @click="emitDeleteBeer">
          <i class="fas fa-minus-circle remove-beer"
             title="remove beer">
          </i>
        </span>
        <span class="float-right action-btn" style="margin-right: 0.35rem;" @click="goToBeer">
          <i class="fas fa-pen" style="color: forestgreen;" title="edit beer"></i>
        </span>
      </h5>
      <p :class="[(beer.description || '').trim().length < 1 ? 'no-desc': 'desc']">{{ beer.description || 'no description available, click pen to edit' }}</p>

    </b-media>
  </b-list-group-item>
</template>

<script>
  import api from '../../modules/api';
  export default {
    name: "beer-preview",
    mounted(){
      this.getThumbnailUrl();
      hook.bp=this;
    },

    props: {
      beer: {
        type: Object,
        default(){
          return {};
        }
      }
    },
    data(){
      return {
        thumbnailUrl: null
      }
    },
    methods: {
      goToBeer(){
        console.log('going to beer! ', this.beer.id);
        this.$router.push({ name: 'editableBeerInfo', params: { beer_id: this.beer.id } })

      },

      async emitDeleteBeer(){
        this.$emit('delete-beer', this.beer.id);
        console.log('deleting beer with id: ', this.beer.id)
      },

      async getThumbnailUrl(){
        const photos = await api.getBeerPhotos(this.beer.id);
        console.log('beer photos: ', photos);
        if (photos.length){
          console.log('setting photo url: ', api.getPhotoUrl(photos[0].id));
          this.thumbnailUrl = api.getPhotoUrl(photos[0].id, true)
        }
      }
    }
  }
</script>

<style scoped>
  .desc {
    color: gray;
  }
  .no-desc {
    color: darkgray !important;
    font-style: italic;
  }
  .no-img {
    color: lightgray;
    font-size: 128px;
  }

  .action-btn {
    cursor: pointer;
    font-size: 1.25rem;
  }

  .remove-beer {
    color: red;
  }

</style>