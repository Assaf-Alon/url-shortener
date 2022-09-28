import { shallowMount, VueWrapper, MountingOptions } from "@vue/test-utils";
import GenericForm from "@/components/GenericForm.vue";

describe("GenericForm.vue", () => {
  let wrapper: VueWrapper;

  //   function createComponent() {
  //     wrapper = shallowMount(GenericForm, {
  //       data: {},
  //       propsData: {},
  //     });
  //   }

  afterEach(() => {
    wrapper.unmount();
  });

  it("renders all fields passed", () => {});
});
