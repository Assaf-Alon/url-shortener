import { shallowMount, VueWrapper, MountingOptions } from "@vue/test-utils";
import GenericForm from "@/components/GenericForm.vue";
import { RULES } from "@/utilities/consts";

describe("GenericForm.vue", () => {
  let wrapper: VueWrapper;

  function createComponent(props: any, data?: any, slots?: any) {
    // wrapper = shallowMount(GenericForm, {
    //   data() {
    //     return data;
    //   },
    //   props: props,
    //   slots: slots,
    // });
  }

  afterEach(() => {
    wrapper.unmount();
  });

  it("renders all fields passed", () => {
    // createComponent(
    //   {
    //     fields: [
    //       {
    //         name: "t1",
    //         label: "t1",
    //         type: "text",
    //         rules: [RULES.required],
    //       },
    //       {
    //         name: "p1",
    //         label: "p1",
    //         type: "password",
    //       },
    //     ],
    //   },
    //   undefined,
    //   undefined
    // );
    // const field1 = wrapper.get('[data-test="t1"]');
  });
});
