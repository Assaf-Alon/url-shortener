<template>
  <div class="d-flex flex-column text-center">
    <v-spacer />
    <h1>ABC URL Shortener</h1>
    <h2>Sign up</h2>
    <GenericForm ref="form" :fields="fields" @submitted="signupAttempt">
      <template v-slot:actions>
        <v-btn type="submit">Sign up</v-btn>
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
import { RuleFunction } from "@/utilities/types";
import DL from "@/utilities/DL";
import GenericForm from "@/components/GenericForm.vue";

export default defineComponent({
  name: "SignInPage",
  data() {
    return {
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
          rules: [RULES.required, RULES.passwordFormat],
        },
        {
          name: "confirm_password",
          label: "Confirm Password",
          type: "password",
          rules: [RULES.required, this.confirmPasswordRule as RuleFunction],
        },
        {
          name: "email",
          label: "Email",
          type: "text",
          rules: [RULES.required, RULES.emailFormat],
        },
      ],
      userID: null,
    };
  },
  methods: {
    ...mapActions(["setUserId"]),
    async signupAttempt(signupInfo: {
      username: string;
      password: string;
      email: string;
    }) {
      let signupResponse = await DL.createUser(
        signupInfo.username,
        signupInfo.password,
        signupInfo.email
      );
      console.log(signupInfo);
      console.log(signupResponse);
      if (signupResponse !== true) {
        // TODO: better notif
        alert(signupResponse);
      }
      this.$router.push("SignIn");
    },
    confirmPasswordRule(v: string): boolean | string {
      let form = this.$refs.form as {
        fieldValues: { [k: string]: string | null };
      };
      let password = form.fieldValues.password;

      return v === password || "Passwords do not match";
    },
  },
  components: {
    GenericForm,
  },
});
</script>
