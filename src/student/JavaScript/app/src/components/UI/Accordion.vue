<template>
  <div class="mb-1 mt-1 w-100">
    <div>

      <!--  DEFAULT HEADER, USE SLOT TO OVERRIDE BUT MUST HANDLE TOGGLE MANUALLY IN HEADER (accordion.toggle())-->

      <div @click="collapsed = !collapsed"
           class="w-100 accordion-header"
           :title="`${collapsed ? 'expand': 'collapse'} content`">
        <span class="float-left ml-2 action-btn" @click.stop="$emit('action-btn-clicked')">
          <slot name="action_btn"></slot>
        </span>
        {{ header }}
        <span class="float-right mr-2">
          <font-awesome-icon prefix="fas" :icon="`angle-${collapsed ? 'down': 'up'}`" class="default-icon" />
        </span>

      </div>

    </div>

    <b-collapse :id="`accordion-${_uid}`"
                @show="emitShow"
                @hide="emitHide"
                v-model="showCollapse">

      <!-- DEFAULT CONTENT SLOT -->
      <slot>
        <p>default body: use body slot</p>
      </slot>
    </b-collapse>
  </div>

</template>

<script>
  export default {
    name: "accordion",
    props: {
      header: {
        type: String,
        default: "Header"
      },
      expanded: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        collapsed: this.expanded || false
      };
    },
    methods: {
      emitShow(){
        this.$emit('show');
        this.$emit('toggle', true);
      },
      emitHide(){
        this.$emit('hide');
        this.$emit('toggle', false);
      },
      expand(){
        this.collapsed = false;
        this.emitShow();
      },

      collapse(){
        this.collapsed = true;
        this.emitHide();
      },

      toggle(){
        this.collapsed = !this.collapsed;
        this.$emit('toggle', this.collapsed);
      }
    },

    computed: {
      showCollapse: {
        get(){
          return !this.collapsed;
        },

        set(){
          return !this.collapsed;
        }

      }
    }
  };
</script>

<style scoped>

  .action-btn{
    font-size: 1.25rem;
    color: white;
    cursor: pointer;
  }

  .default-icon{
    font-size: 1.25rem;
  }

  .accordion-header {
    font-size: 1.1rem;
    font-weight: bold;
    /*color: gray;*/
    color: white;
    background-color: forestgreen;
    padding: 0.3rem;
    cursor: pointer;
  }
</style>