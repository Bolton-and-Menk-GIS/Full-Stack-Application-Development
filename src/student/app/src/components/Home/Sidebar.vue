<template>
  <div id="sidebar" :class="{'active': active}"
       :style="{width: `${expandWidth}px`, display: active ? 'block': 'none'}">

    <!--  DEFAULT SIDEBAR CONTENT GETS INSERTED IN SLOT BELOW-->
    <slot></slot>

  </div>
</template>

<script>
  import { EventBus } from "../../modules/EventBus";

  export default {
    name: "sidebar",
    props: {
      expandWidth: {
        type: Number,
        default: 350
      }
    },
    data() {
      return {
        active: false,
        hiddenWidth: 0
      }
    },
    mounted(){
      console.log('MOUNTED SIDEBAR: ', this);
      
      EventBus.$on('toggle-menu', (toggleOn)=>{
        if (toggleOn === undefined){
          this.active = !this.active;
        } else {
          this.active = toggleOn;
        }

      });
    },
    methods: {
      expand(){
        this.active = true;
      },

      collapse(){
        this.active = false;
      },

      toggle(){
        this.active = !this.active;
      }
    },
    watch: {
      active(newVal){
        this.$emit('toggled', newVal);
        this.$emit(newVal ? 'expanded': 'collapsed');
      }
    }
  }
</script>

<style scoped>
  #sidebar{
    display: block;
    background: whitesmoke;
    height: calc(100vh - 60px);
    overflow-y: scroll;
  }

  #sidebar.active {
    display: block;
  }
  #sidebar a {
    display: block;
    padding: 10px 5px;
    color: #666;
    border-bottom: 1px solid #bbb;
  }
</style>