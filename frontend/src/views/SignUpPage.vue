<template>
  <GenericForm></GenericForm>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import GenericForm from "@/components/GenericForm.vue";

export default defineComponent({
  name: "SignUpPage",
  components: {
    GenericForm,
  },
});
</script>
