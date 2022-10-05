export const RULES = {
  required: function (v: string) {
    return Boolean(v) || "Required";
  },
  passwordFormat: function (v: string) {
    const length = v.length;
    const numLowercase = v.match(/[a-z]/g)?.length || 0;
    const numUppercase = v.match(/[A-Z]/g)?.length || 0;
    const numDigits = v.match(/[0-9]/g)?.length || 0;
    const numSpecial = v.match(/[!@#$%^&*()_+]/g)?.length || 0;

    console.log({ length, numLowercase, numUppercase, numDigits, numSpecial });
    if (length < 8) return "Password not long enough";
    if (numLowercase < 2) return "Must have 2 lowercase letters";
    if (numUppercase < 2) return "Must have 2 uppercase letters";
    if (numDigits < 2) return "Must have 2 digits";
    if (numSpecial < 2) return "Must have 2 special characters";

    return true;
  },
  emailFormat: function (v: string) {
    return (
      /^[a-zA-Z][a-zA-Z0-9\\.]*@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$/.test(v) ||
      "Email Format Required"
    );
  },
  shortUrlFormat: function (v: string) {
    return /^[a-zA-Z0-9]+$/.test(v) || "Can only use characters and digits";
  },
  longUrlFormat: function (v: string) {
    return (
      /^www(\.[a-zA-Z0-9]+){2,}$/.test(v) ||
      "Must be in world wide web format (www.xxx.xxx...)"
    );
  },
};

export const BASE_URL = "abc.sh/";
