<template>
  <div class="d-flex flex-column text-center full-width">
    <v-spacer />
    <h1>ABC URL Shortener</h1>
    <h2>Logged in as {{ getUserId }}</h2>
    <v-spacer />
    <SingleURL v-for="url in urls" :key="url.short_url" :url="url"></SingleURL>
    <v-spacer />
    <NewURL></NewURL>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import DL from "@/utilities/DL";
import { URLResponse } from "@/utilities/types";
import SingleURL from "@/components/SingleURL.vue";
import NewURL from "@/components/NewURL.vue";
import { mapGetters } from "vuex";
export default defineComponent({
  name: "HomePage",
  data() {
    return {
      urls: [] as URLResponse[],
    };
  },
  computed: {
    ...mapGetters(["getUserId"]),
  },
  methods: {
    async getURLS() {
      let resp = await DL.getUserUrlTranslations();
      console.log(resp);

      return resp;
    },
  },
  async created() {
    this.urls = await this.getURLS();
  },
  components: { SingleURL, NewURL },
});
</script>

<style>
.full-width {
  width: 100%;
}
</style>
