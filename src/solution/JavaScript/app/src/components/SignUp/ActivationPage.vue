<template>
  <div class="activation">
    <b-card class="w-75 mx-auto mt-4 activation-card">

      <div class="loading mt-4" v-if="state === 'checking'">
        <spinner text="loading..." :visible="true" />
      </div>

      <div class="default" v-if="state === 'default'">
        
        <div class="mt-2" v-if="userIsActivated">
          <p class="mt-2 theme">Your account has already been activated!</p>
          <b-button class="theme mt-4" @click="navigateToMap">Go Back</b-button>
        </div>

        <div class="not-activated" v-else>
          <h4 class="theme mt-2">Activate Your Account</h4>
          <p class="mt-2 activation">Thank you for registering with Brewery Finder.  To complete your account setup please click the button below.</p>
          <b-button class="theme mt-4" @click="activate">Activate My Account</b-button>
        </div>
        
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
  import swal from 'sweetalert2';

  export default {
    name: "activation-page",

    data(){
      return {
        state: 'checking',
        userIsActivated: false
      }
    },

    // we want to check if the user is already activated
    beforeRouteEnter(to, from, next){
      console.log('BEFORE ACTIVATION PAGE ENTER: ', to, from, next);
      next(async (vm) => {
        // check status first
        vm.userIsActivated = await vm.checkStatus(to.params.id);
        console.log('STATUS: ', vm.userIsActivated);

        // now call next() to actually navigate to this route
        next();
      });

    },

    methods: {

      async checkStatus(id){
        this.status = 'checking';
        try {
          const resp = await api.userIsActive(id || this.id);
          this.state = 'default';
          return resp;
        } catch (err){
          // user does not exist?
          swal({
            title: 'User does not exist!',
            type: 'error',
          }).then((result)=>{
            this.navigateToMap();
          });
        }
        
      },
    
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