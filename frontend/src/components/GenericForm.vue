<template>
  <v-form
    v-model="valid"
    class="form"
    @submit.prevent="$emit('submitted', fieldValues)"
  >
    <v-text-field
      v-for="field in fields"
      :data-test="field.name"
      v-model="fieldValues[field.name]"
      :label="field.label"
      :key="field.name"
      :rules="field.rules"
      :type="visible[field.name] ? 'text' : field.type"
      :append-icon="appendIcon(field)"
      @click:append="() => (visible[field.name] = !visible[field.name])"
      clearable
    >
    </v-text-field>

    <slot v-if="actionsSupplied" name="actions" />
    <v-btn v-else type="submit">Submit</v-btn>
  </v-form>
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
  emits: ["submitted"],
  data() {
    return {
      valid: null,
      visible: {} as {
        [k: string]: boolean;
      },
      fieldValues: {} as {
        [k: string]: string | null;
      },
    };
  },
  computed: {
    actionsSupplied() {
      return Boolean(this.$slots["actions"]);
    },
  },
  created() {
    if (!this.fields) return;

    this.visible = Object.fromEntries(
      this.fields
        .filter((field) => field.type === "password")
        .map((field) => {
          return [field.name, false];
        })
    );

    this.fieldValues = Object.fromEntries(
      this.fields.map((field) => {
        return [field.name, null];
      })
    );
  },
  methods: {
    appendIcon(field: FormField) {
      if (field.type != "password") return;
      return this.visible[field.name] ? "mdi-eye-off" : "mdi-eye";
    },
  },
  components: {},
});
</script>
<style>
.form {
  width: 400px;
}
</style>
