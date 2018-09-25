<template>
  <div class="activation">
    <b-card class="w-75 mx-auto mt-4 activation-card">
      <div class="default" v-if="state === 'default'">
        <h4 class="theme mt-2">Activate Your Account</h4>
        <p class="mt-2 activation">Thank you for registering with Brewery Finder.  To complete your account setup please click the button below.</p>
        <b-button class="theme mt-4" @click="activate">Activate My Account</b-button>
      </div>

      <div class="mt-2" v-else>
        <spinner :visible="state === 'activating'" text="Activating your account..." />
        <b-alert :show="1" @dismissed="navigateToMap" v-if="state === 'activated'" variant="success">Successfully Activated Account</b-alert>
        <b-alert :show="1" @dismissed="state = 'default'" v-if="state === 'error'" variant="danger">Account Activation Failed, please try again.</b-alert>
      </div>

    </b-card>
  </div>
</template>

<script>
  import api from '../../modules/api';
  import Spinner from '../UI/Spinner';

  export default {
    name: "activation-page",
    components: { Spinner },
    mounted(){hook.a = this;},
    data(){
      return {
        state: 'default'
      }
    },
    methods: {
      async activate(){
        this.state = 'activating';
        try {
          const resp = await api.activate(this.id);
          console.log('ACTIVATION RESPONSE: ', resp);
          this.state = 'activated';
        } catch(err){
          this.state = 'error';
        }
      },

      navigateToMap(){
        this.$router.push({ name: 'home' });
      }
    },
    computed: {
      id(){
        return this.$route.params.id;
      }
    }
  }
</script>

<style scoped>
  .activation-card {
    background-color: whitesmoke;
    padding: 1rem;
  }

  .activation {
    font-family: Verdana, Geneva, sans-serif;
    color: gray;
    font-size: 1.15rem;
  }



</style>