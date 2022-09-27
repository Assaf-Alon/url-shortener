<template>
  <GenericForm :fields="fields" submit-btn-label="OK">
    <template v-slot:actions>
      <div>
        <v-btn type="submit">Login</v-btn>
        <v-btn @click="$router.push('signUp')">Sign Up</v-btn>
      </div>
      <v-btn>Login with google</v-btn>
    </template>
  </GenericForm>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import { RULES } from "@/utilities/consts";
import GenericForm from "@/components/GenericForm.vue";

export default defineComponent({
  name: "SignInPage",
  data() {
    return {
      fields: [
        {
          name: "user",
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
  },
  components: {
    GenericForm,
  },
});
</script>
