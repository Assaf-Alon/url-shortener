<template>
  <GenericForm :fields="fields"></GenericForm>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import GenericForm from "@/components/GenericForm.vue";

export default defineComponent({
  name: "SignInPage",
  data() {
    return {
      fields: [
        {
          name: "user",
          label: "username",
        },
        {
          name: "user",
          label: "username",
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
