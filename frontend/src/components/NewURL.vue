<template>
  <v-form v-model="valid" ref="form">
    <v-row class="align-center">
      <v-col cols="grow">
        <v-text-field
          label="Long Url"
          v-model="long_url"
          variant="outlined"
          class="pa-2 flex-shrink-1"
          :rules="[RULES.required, RULES.longUrlFormat]"
        />
      </v-col>

      <v-col cols="auto">
        <v-btn icon flat @click="newURL">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row class="align-center">
      <v-col cols="grow">
        <v-text-field
          label="Short Url"
          persistent-placeholder
          :prefix="BASE_URL"
          v-model="short_url"
          variant="outlined"
          class="pa-2 flex-grow-1 prefix-no-space"
          :readonly="!customURL"
          :rules="
            customURL ? [RULES.required, RULES.shortUrlFormat] : undefined
          "
        />
      </v-col>
      <v-col cols="auto">
        <v-checkbox v-model="customURL" @click="checkboxed" />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import { BASE_URL, RULES } from "@/utilities/consts";

export default defineComponent({
  name: "NewURL",
  data() {
    return {
      BASE_URL: BASE_URL,
      short_url: "",
      users_short_url: "",
      long_url: "",
      customURL: false,
      RULES: RULES,
      valid: false,
    };
  },
  methods: {
    checkboxed() {
      let form = this.$refs.form as {
        validate: () => Promise<{ valid: boolean }>;
      };
      form.validate();
      if (this.customURL) {
        this.users_short_url = this.short_url;
        this.short_url = this.long_url.split(".").join("");
      } else {
        this.short_url = this.users_short_url;
      }
    },
    newURL() {
      let form = this.$refs.form as {
        validate: () => Promise<{ valid: boolean }>;
      };
      form.validate();

      if (this.valid) {
        this.$emit("newURL", {
          short_url: this.short_url,
          long_url: this.long_url,
        });
      }
    },
  },
  watch: {
    long_url() {
      if (!this.customURL) {
        this.short_url = this.long_url.split(".").join("");
      }
    },
  },
  components: {},
});
</script>
