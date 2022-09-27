export const RULES = {
  required: function (v: string) {
    return Boolean(v) || "Required";
  },
};
