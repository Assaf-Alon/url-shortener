<template>
  <v-card class="d-flex flex-row">
    <v-col cols="2">
      <v-text-field
        :modelValue="url.short_url"
        readonly
        variant="outlined"
        id="shortUrl"
        class="pa-2 flex-shrink-1"
        hide-details
        append-icon="mdi-content-copy"
        @click:append.prevent="copyShortUrl"
      />
    </v-col>
    <v-col cols="grow">
      <v-text-field
        :modelValue="url.long_url"
        readonly
        variant="outlined"
        class="pa-2 flex-shrink-1"
        hide-details
      />
    </v-col>
    <v-col cols="auto" class="d-flex align-center">
      <v-btn icon flat @click="$emit('delete')">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
      <EditURL :url="url" @edit="edit" />
      {{ views }} <v-icon color="grey">mdi-eye</v-icon>
    </v-col>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { URLResponse } from "@/utilities/types";
import EditURL from "@/components/EditURL.vue";

export default defineComponent({
  name: "SingleURL",
  emits: {
    delete() {
      return true;
    },
    edit({ short_url, long_url }: { short_url: string; long_url: string }) {
      return (
        /^abc.sh/.test(short_url) &&
        short_url.split("/")[1].length > 0 &&
        long_url.length > 0
      );
    },
  },
  props: {
    url: {
      type: Object as () => URLResponse,
      required: true,
    },
  },
  data() {
    return {
      views: 100,
    };
  },
  methods: {
    edit(event: { short_url: string; long_url: string }) {
      if (
        event.short_url === this.url.short_url &&
        event.long_url === this.url.long_url
      )
        return;

      this.$emit("edit", event);
    },
    copyShortUrl() {
      navigator.clipboard.writeText(this.url.short_url);
    },
  },
  components: {
    EditURL,
  },
});
</script>
