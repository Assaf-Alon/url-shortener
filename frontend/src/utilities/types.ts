interface urlTranslation {
  shortURL: string;
  LongURL: string;
}

type userID = string | null;

interface URLResponse {
  short_url: string;
  long_url: string;
  user_id: userID;
}

interface RuleFunction {
  (v: any): true | string;
}

interface FormFieldInterface {
  name: string;
  label: string;
  rules?: RuleFunction[];
  type?: string;
}

class FormField implements FormFieldInterface {
  name: string;
  label: string;
  rules?: RuleFunction[];
  type?: string;
  constructor(
    name: string,
    label: string,
    rules?: RuleFunction[],
    type?: string
  ) {
    this.name = name;
    this.label = label;
    this.rules = rules;
    this.type = type;
  }
}

export { urlTranslation, userID, URLResponse, FormField, RuleFunction };
