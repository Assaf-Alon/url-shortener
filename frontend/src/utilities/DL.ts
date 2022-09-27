import store from "@/store";
import { URLResponse } from "@/utilities/types";

const BASE_URL = "http://localhost:5000/";

export async function getUserUrlTranslations(): Promise<URLResponse[]> {
  //   return await fetch(BASE_URL + "/get_user_urls/" + store.getters.getUserId);
  return [
    {
      short_url: "abc.sh/asd",
      long_url: "www.youtube.com",
      user_id: store.getters.getUserId,
    },
    {
      short_url: "abc.sh/asdb",
      long_url: "www.reddit.com",
      user_id: store.getters.getUserId,
    },
  ];
}

export default { getUserUrlTranslations };
