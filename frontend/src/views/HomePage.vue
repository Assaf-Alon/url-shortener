<template>
  <SingleURL></SingleURL>
  <NewURL></NewURL>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import DL from "@/utilities/DL";
import { URLResponse } from "@/utilities/types";
import SingleURL from "@/components/SingleURL.vue";
import NewURL from "@/components/NewURL.vue";
export default defineComponent({
  name: "HomePage",
  data() {
    return {
      urls: [] as URLResponse[],
    };
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
