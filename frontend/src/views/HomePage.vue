<template>
  <div class="d-flex flex-column text-center full-width full-height">
    <v-spacer />
    <h1>ABC URL Shortener</h1>
    <h2>Logged in as {{ getUserId }}</h2>
    <v-spacer />
    <div style="height: min-content; overflow: auto">
      <SingleURL
        v-for="url in urls"
        :key="url.short_url"
        :url="url"
        @delete="deleteUrl(url)"
        @edit="editUrl"
      />
    </div>
    <v-spacer />
    <NewURL class="pa-5" @newURL="createNewURL" />
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
    async reloadURLS() {
      this.urls = [...(await this.getURLS())];
    },
    async createNewURL({
      short_url,
      long_url,
    }: {
      short_url: string;
      long_url: string;
    }) {
      let resp = await DL.createUserTranslation(short_url, long_url);

      console.log(resp);

      this.reloadURLS();
    },
    async deleteUrl({ short_url, long_url }: URLResponse) {
      let resp = await DL.deleteUserTranslation(short_url, long_url);
      console.log(resp);

      this.reloadURLS();
      return;
    },
    async editUrl(event: { short_url: string; long_url: string }) {
      this.reloadURLS();
      return;
    },
  },
  async created() {
    this.reloadURLS();
  },
  components: { SingleURL, NewURL },
});
</script>

<style>
.full-width {
  width: 100%;
}
.full-height {
  height: 100vh;
}
</style>
