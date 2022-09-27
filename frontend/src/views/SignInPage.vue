<template>
  <label for="input">username: </label>
  <input id="input" v-model="userID" />
  <button
    type="submit"
    @click="
      setUserId(userID);
      $router.push('/');
    "
  >
    ok
  </button>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapActions } from "vuex";

export default defineComponent({
  name: "SignInPage",
  data() {
    return {
      userID: null,
    };
  },
  methods: {
    ...mapActions(["setUserId"]),
  },
  components: {
    // HelloWorld,
  },
});
</script>
