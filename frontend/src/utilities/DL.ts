import store from "@/store";
import { URLResponse } from "@/utilities/types";
import axios from "axios";

const BASE_URL = "http://localhost:5000/";

export async function getUserUrlTranslations(): Promise<URLResponse[]> {
  try {
    const response = await axios.get(
      BASE_URL + "/get_user_urls/" + store.getters.getUserId
    );
    console.log(response);

    return response.data;
  } catch (err) {
    debugger;
    console.log(err);
  }
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
