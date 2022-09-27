<template>
  <v-text-field v-for="field in fields" :key="field.name"> </v-text-field>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { FormField } from "@/utilities/types";

export default defineComponent({
  name: "GenericForm",
  props: {
    fields: {
      type: Array as () => Array<FormField>,
    },
  },
  data() {
    return {};
  },
  methods: {},
  components: {},
});
</script>
