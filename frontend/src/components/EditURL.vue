<template>
  <v-btn icon flat @click="edit">
    <v-icon>mdi-pencil</v-icon>
  </v-btn>
  <v-dialog v-model="popup">
    <v-card class="popup-card">
      <v-card-title>Edit URL</v-card-title>
      <v-card-text>
        <v-form v-model="valid" ref="form">
          <v-text-field
            :prefix="BASE_URL"
            v-model="new_short_url"
            variant="outlined"
            class="pa-2 flex-shrink-1 prefix-no-space"
            :rules="[RULES.required, RULES.shortUrlFormat]"
          />
          <v-text-field
            label="Long Url"
            v-model="new_long_url"
            variant="outlined"
            class="pa-2 flex-shrink-1"
            :rules="[RULES.required, RULES.longUrlFormat]"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn flat @click="save">
          <v-icon> mdi-content-save </v-icon>
          save
        </v-btn>
        <v-btn flat @click="cancel">
          <v-icon> mdi-cancel </v-icon>
          cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { URLResponse } from "@/utilities/types";
import { BASE_URL, RULES } from "@/utilities/consts";

export default defineComponent({
  name: "EditURL",
  emits: {
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
      popup: false,
      new_short_url: "",
      new_long_url: "",
      BASE_URL: BASE_URL,
      RULES: RULES,
      valid: false,
    };
  },
  methods: {
    edit() {
      this.popup = true;
      this.new_short_url = this.url.short_url.split("/")[1];
      this.new_long_url = this.url.long_url;
    },
    save() {
      let form = this.$refs.form as {
        validate: () => Promise<{ valid: boolean }>;
      };
      form.validate();
      if (!this.valid) return;
      this.popup = false;
      this.$emit("edit", {
        short_url: BASE_URL + this.new_short_url,
        long_url: this.new_long_url,
      });
    },
    cancel() {
      this.popup = false;
    },
  },
  components: {},
});
</script>

<style scoped>
.popup-card {
  width: 50rem;
  margin: auto;
}
</style>

<style>
.v-text-field--prefixed.prefix-no-space .v-field__input {
  padding-inline-start: unset;
}

.prefix-no-space .v-text-field__prefix {
  opacity: 1;
}
</style>
