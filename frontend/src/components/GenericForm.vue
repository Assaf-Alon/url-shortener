<template></template>

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
