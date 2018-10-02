<template>
  <b-navbar toggleable="md" type="dark" class="theme-banner app-header" :sticky="true">
    <b-navbar-brand href="#"><strong>Brewery Finder</strong></b-navbar-brand>

    <b-navbar-nav class="ml-auto">

      <!-- ICON FOR DATA DOWNLOAD -->
      <span v-if="userLoggedIn" v-b-modal.export-modal>
        <i class="fas fa-external-link-alt mr-2 download-btn app-nav-btn"
           title="export brewery data">
        </i>
      </span>

      <!-- ICON FOR HANDLING LOGIN -->
      <span @click="userLoggedIn ? logout(): showLoginModal = true"
            :title="`sign ${ userLoggedIn ? 'out': 'in' }`">
        <font-awesome-icon
                prefix="fas"
                icon="user-circle"
                :class="['login-btn', 'app-nav-btn', {'logged-in': userLoggedIn}]">
        </font-awesome-icon>
      </span>

    </b-navbar-nav>

    <!--  LOGIN MODAL -->
    <b-modal id="login-modal" :hide-footer="true" ref="loginModal" v-model="showLoginModal">
      <login-page @user-logged-in="handleLogin" @dismiss-login-modal="dismissLogin"></login-page>
    </b-modal>

    <!-- LOGOUT MODAL -->
    <b-modal id="logout-modal" v-model="showLogout" :hide-footer="true">
      <div class="logout-container">
        <spinner :text="'Logging Out'" :visible="state === 'logging_out'" />
        <b-alert :show="1" v-if="state === 'logged_out'" @dismissed="showLogout = false" variant="success">Successfully Logged Out</b-alert>
      </div>
    </b-modal>

    <!-- PLACEHOLDER FOR EXPORT DATA MODAL -->
    <export-data />

  </b-navbar>
</template>

<script>
  import { EventBus } from '../modules/EventBus';
  import LoginPage from './Home/LoginPage';
  import api from '../modules/api';
  import ExportData from './ExportData';

  export default {
    name: "app-nav-bar",
    components: {
      LoginPage,
      ExportData
    },
    data() {
      return {
        state: null,
        showLoginModal: false,
        userLoggedIn: false,
        showLogout: false,
      }
    },
    async mounted(){
      console.log('MOUNTED APP NAV BAR: ', this);

      // check if user is already logged in via the remember me token cookie
      try {
        const resp = await api.authTest();
        if (resp.status === 'success'){
          this.userLoggedIn = true;
        }
      } catch (err){
        // ignore, just means user isn't authenticated from a prior session
      }
    },

    methods: {
      async logout(){
        this.showLogout = true;
        this.state = 'logging_out';
        const resp = await api.logout();
        this.userLoggedIn = false;
        this.state = 'logged_out';

        // bubble up logout event
        EventBus.$emit('user-logged-out');
        return resp;
      },

      dismissLogin(){
        this.$refs.loginModal.hide();

        // for some reason the modal dismiss was causing a race condition and interfering with the router...
        setTimeout(()=>{
          this.$router.push({name: 'signup'});
        }, 100)
      },

      handleLogin(){
        this.userLoggedIn = true;
        this.state = 'logged_in';
        this.showLoginModal = false;

        // bubble up login event
        EventBus.$emit('user-logged-in');
      },

    },
  }
</script>

<style scoped>
  .logout-container {
    margin: auto;
    margin-top: 2rem;
    margin-bottom: 2rem;
  }

  .app-nav-btn {
    font-size: 2.5rem;
    color: white;
    cursor: pointer;
  }

  .login-btn:hover{
    background-color: orange;
    font-weight: bold;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
    color: lightgray;
  }

  .logged-in{
    color: orange !important;
    background-color: white;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
  }

  .logged-in:hover {
    color: darkorange !important;
    background-color: lightgray !important;
  }

</style>