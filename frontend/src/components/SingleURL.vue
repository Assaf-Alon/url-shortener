<template>
  <v-card class="d-flex flex-row">
    <v-text-field
      :value="url.short_url"
      readonly
      variant="outlined"
      class="pa-2 shrink"
      hide-details
      style="width: max-content"
    ></v-text-field>
    <v-text-field
      :value="url.long_url"
      readonly
      variant="outlined"
      class="pa-2"
    ></v-text-field>

    <EditURL></EditURL>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { URLResponse } from "@/utilities/types";
import EditURL from "@/components/EditURL.vue";

export default defineComponent({
  name: "SingleURL",
  props: {
    url: {
      type: Object as () => URLResponse,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {},
  components: {
    EditURL,
  },
});
</script>
