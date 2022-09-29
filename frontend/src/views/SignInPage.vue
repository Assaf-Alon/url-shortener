<template>
  <div class="d-flex flex-column">
    response is: {{ response }}
    <v-spacer />
    <h1>ABC URL Shortener</h1>
    <GenericForm :fields="fields" @submitted="loginAttempt">
      <template v-slot:actions>
        <div>
          <v-btn type="submit">Login</v-btn>
          <v-btn @click="$router.push('signUp')">Sign Up</v-btn>
        </div>
        <v-btn>Login with google</v-btn>
      </template>
    </GenericForm>
    <v-spacer />
    <v-spacer />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import { RULES } from "@/utilities/consts";
import GenericForm from "@/components/GenericForm.vue";
import DL from "@/utilities/DL";

export default defineComponent({
  name: "SignInPage",
  data() {
    return {
      response: [] as any[],
      fields: [
        {
          name: "username",
          label: "Username",
          type: "text",
          rules: [RULES.required],
        },
        {
          name: "password",
          label: "Password",
          type: "password",
          rules: [RULES.required],
        },
      ],
      userID: null,
    };
  },
  methods: {
    ...mapActions(["setUserId"]),
    loginAttempt(loginInfo: { username: string; password: string }) {
      this.setUserId(loginInfo.username);
      this.$router.push("/");
    },
  },
  async created() {
    this.response = await DL.getUserUrlTranslations();
  },
  components: {
    GenericForm,
  },
});
</script>
