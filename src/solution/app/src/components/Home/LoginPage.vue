<template>
  <div class="login-container">
    <b-card class="login-card" v-if="state === 'default'">
      <b-img src="./assets/avatar_2x.png" class="avatar"></b-img>

      <div class="mt-4">
        <b-form-input v-model="username" placeholder="username"></b-form-input>
        <b-form-input type="password" v-model="password" placeholder="password" class="mt-2 mb-4"></b-form-input>

        <b-form-checkbox v-model="rememberMe" style="color: white;">Remember Me</b-form-checkbox>

        <b-button block class="sign-in-btn mt-4 mb-4" @click="login">Sign In</b-button>
      </div>

      <hr style="background-color: white;">

      <!--  SIGN UP LINK -->
      <!--  @click=$emit('sign-up')-->
      <p class="acc">Don't have an Account? <a href="#" class="sign-up" @click="$emit('dismiss-login-modal')">Sign Up</a></p>

    </b-card>

    <div v-else>
      <spinner :visible="state === 'logging_in'" :text="'Logging In...'"/>

      <b-alert :show="1" @dismissed="handleUserLogin"
               v-if="state === 'logged_in'"
               variant="success">
        Successfully Logged In
      </b-alert>

      <b-alert :show="1" @dismissed="state = 'default'"
               v-if="state === 'login_failed'"
               variant="danger">
        Login Failed, please try again.
      </b-alert>

    </div>

  </div>
</template>

<script>
  import api from '../../modules/api';
  import Spinner from '../UI/Spinner';

  export default {
    name: "login-page",
    components: {
      Spinner,
    },
    data(){
      return {
        username: null,
        password: null,
        rememberMe: false,
        state: 'default'
      }
    },

    methods: {
      login: async function(){
        this.state = 'logging_in';
        try {
          const result = await api.login(this.username, this.password, this.rememberMe);
          if (result.status === 'success'){
            this.state = 'logged_in';
          }
        }

        catch(err) {
          this.state = 'login_failed';
        }
      },

      handleUserLogin(){
        this.$emit('user-logged-in');
        // do a short timeout before switching state back to normal so user doesn't see
        // login screen again.
        setTimeout(()=>{
          this.state = 'default';
        }, 500);
      }
    }
  }
</script>

<style scoped>

  .avatar {
    border-radius: 50%;
    height: 5rem;
  }

  .login-card {
    padding: 2rem;
    background-color: rgba(34,139,34, .75);
  }

  .sign-in-btn {
    background-color: orange;
    border-color: orange;
    font-weight: bold;
  }

  .sign-in-btn:hover {
    /*opacity: 0.5;*/
    background-color: darkorange;
  }

  .login-container {
    /*max-width: 350px;*/
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
    width: 75%;
    margin: auto;
  }

  .acc {
    color: white;
    font-size: 0.85rem;
  }

  .sign-up {
    color: orange;
    font-weight: bold;
    font-size: 0.9rem;
  }

  .sign-up:hover {
    color: darkorange;
  }

</style>