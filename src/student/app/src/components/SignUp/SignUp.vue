<template>
  <div class="jumbotron signup-container mb-0">
    <h3 class="theme">Sign Up for Brewery Finder</h3>
    <b-card class="mx-auto p-4 signup-card">
      <b-form class="signup-form" v-if="state === 'default'" @submit="submit">
        <b-form-group label="Name:" label-text-align="left">
          <b-form-input type="text"
                        v-model.trim="name"
                        :state="!$v.name.$invalid"
                        aria-describedby="nameRequired"/>
          <b-form-invalid-feedback id="nameRequired">
            Name is Required
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Email:" label-text-align="left">
          <b-form-input type="email"
                        v-model.trim="email"
                        :state="!$v.email.$invalid"
                        aria-describedby="invalidEmail"/>
          <b-form-invalid-feedback id="invalidEmail">Invalid email address</b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Username:" label-text-align="left">
          <b-form-input type="text" 
            v-model.trim="username" 
            :state="!$v.username.$invalid" 
            aria-describedby="tooShort"/>
          <b-form-invalid-feedback id="tooShort">{{ invalidUsernameFeedback }}</b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Password:" label-text-align="left">
          <b-form-input type="password"
                        v-model.trim="password"
                        aria-describedby="strongFeedback"
                        :state="!$v.password.$invalid"/>
          <b-form-invalid-feedback id="strongFeedback">Password must be at least 8 characters long and contain letters and numbers</b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Retype Password:" label-text-align="left">
          <b-form-input type="password"
                        v-model.trim="passwordVerify"
                        aria-describedby="retypeFeedback"
                        :state="!$v.passwordVerify.$invalid" />
          <b-form-invalid-feedback id="retypeFeedback">Passwords do not match</b-form-invalid-feedback>
        </b-form-group>

        <b-btn class="theme mt-2" :disabled="!formIsValid">Sign Up</b-btn>
        <b-btn variant="danger mt-2 ml-4 bold" @click="$router.push({name: 'home'})">Cancel</b-btn>
      </b-form>

      <!-- LOADING SPINNER -->
      <spinner :visible="state === 'loading'"  text="One moment please..."/>

      <div class="mt-2" v-if="state === 'registered'">
        <h5 class="theme">Successfully Registered</h5>
        <p class="mt-2">An activation email was sent to <b>{{ email }}</b>.  Please see email for further instructions.</p>
        <b-btn class="theme mt-4" @click="$router.push({name: 'home'})">Return To Map</b-btn>
      </div>

      <div class="error" v-if="state === 'error'">
        <b-alert :show="1" @dismissed="state = 'default'" variant="danger">Failed to create user, please try again.</b-alert>
      </div>

    </b-card>

  </div>
</template>

<script>
  import api from '../../modules/api';
  import { validationMixin } from "vuelidate"
  import { helpers, required, minLength, sameAs, email } from "vuelidate/lib/validators"

  // custom validators
  const strongPassword = helpers.regex('strongPassword', /^(((?=.*[a-z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{8,})/);

  const usernameNotTaken = (value, vm) => {
    return !vm.usernames.includes(value);
  }

  export default {
    name: "sign-up",
    mixins: [
      validationMixin
    ],
    
    async beforeMount(){
      this.usernames = await api.fetchUsernames();
    },

    data(){
      return {
        usernames: [],
        name: '',
        username: '',
        password: '',
        passwordVerify: '',
        email: '',
        state: 'default',
      }
    },

    validations: {
      name: {
        required
      },

      email: {
        required,
        email
      },

      username: {
        required,
        minLength: minLength(5),
        usernameNotTaken // custom validator!
      },

      password: {
        required,
        strongPassword // custom validator!
      },

      passwordVerify: {
        required,
        sameAsPassword: sameAs('password')
      }

    },

    methods: {

      async submit(){
        this.state = 'loading';
        try {
          const resp = await api.createUser({
            name: this.name,
            email: this.email,
            username: this.username,
            password: this.password,
            activation_url: this.activationUrl
          });
          console.log('CREATE USER RESPONSE: ', resp);
          if (resp.status === 'success'){
            this.state = 'registered';
          } else {
            this.state = 'error';
          }
        } catch(err) {
          console.log('error', err);
          this.state = 'error';
        }
      }
    },

    computed: {

      invalidUsernameFeedback(){
        return this.usernameTaken ? `"${this.username}" is already taken`: 'Username must be at least 5 characters';
      },

      activationUrl(){
        const urlParts = window.location.href.split('/');
        return `${urlParts.slice(0, urlParts.length-1).join('/')}/users/{id}/activate`;
      },

      formIsValid(){
        // disable button until everything is valid
        return [!this.$v.name.$invalid, !this.$v.username.$invalid, !this.$v.email.$invalid, !this.$v.password.$invalid, !this.$v.passwordVerify.$invalid].every(f => !!f);
      }

    }
  }
</script>

<style scoped>

  .signup-container {
    min-height: calc(100vh - 60px);
  }

  @media screen and (max-width: 999px) {
    .signup-card {
      width: 75%;
    }
  }

  @media screen and (min-width: 1000px) {
    .signup-card {
      width: 50%;
    }
  }

</style>