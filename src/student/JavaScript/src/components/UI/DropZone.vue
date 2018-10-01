<template>
  <div class="drop-container w-100">
    <div class="dropzone-container" v-if="dropSupported">
      <div class="dropzone" ref="dropzone"
           :class="dropzoneClass"
           @drop.prevent.stop="handleDrop"
           @dragenter="addHighlight"

           @dragleave="removeHighlight">
        <input type="file" multiple :disabled="isSaving"
               accept="image/*" class="input-file">
        <p v-if="!isSaving">
          Drag your photo here to begin<br> or click to browse
        </p>
      </div>
    </div>

    <div class="manual" v-else>
      <b-form-file v-model="photo" placeholder="Choose a beer image..." />
    </div>

  </div>

</template>

<script>
  export default {
    name: "drop-zone",
    beforeMount(){
      this.dropSupported = ('draggable' in document.createElement('span'));
    },

    data() {
      return {
        files: [],
        photo: null,
        isSaving: false,
        dropSupported: false,
        dropzoneClass: []
      }
    },

    methods: {
      handleDrop(e){
        console.log('dropped!');
        console.log('dropped yo!', e)
        /*
          Capture the files from the drop event and add them to our local files
          array.
        */
        for( let i = 0; i < e.dataTransfer.files.length; i++ ){
          this.files.push( e.dataTransfer.files[i] );
        }
        console.log('FILES: ', this.files);
        this.$emit('received-files', this.files);
      },

      addHighlight(e){
        console.log(e)
        if (!this.dropzoneClass.includes('highlight')){
          this.dropzoneClass.push('highlight');
        }
      },

      removeHighlight(){
        this.dropzoneClass.length = 0;
      }
    }
  }
</script>

<style scoped>
  .dropzone {
    margin: 20px auto;
    border-radius: 10px;
    outline: 2px dashed forestgreen; /* the dash box */
    outline-offset: -10px;
    background: lightcyan;
    color: dimgray;
    padding: 10px 10px;
    min-height: 200px; /* minimum height */
    position: relative;
    cursor: pointer;
  }

  .dropzone:hover {
    background: lightblue; 
  }

  .highlight{
    color: darkgray;
    /*border: 2px dashed darkorange;*/
    background: rgba(255,165,0,.25);
    outline-offset: -10px;
  }
  .dropzone p {
    font-size: 1.1em;
    text-align: center;
    padding: 50px 0;
  }

  .drop-caption {
    margin-top: 30%; color: gray;
  }

  .input-file {
    opacity: 0; /* invisible but it's there! */
    top: 0;
    left: 0;
    width: 100%;
    height: 200px;
    position: absolute;
    cursor: pointer;
  }

</style>