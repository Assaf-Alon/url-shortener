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
}

class FormField implements FormFieldInterface {
  name: string;
  label: string;
  rules?: RuleFunction[];
  constructor(name: string, label: string, rules: RuleFunction[]) {
    this.name = name;
    this.label = label;
    this.rules = rules;
  }
}

export { urlTranslation, userID, URLResponse, FormField };
