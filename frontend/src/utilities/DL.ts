import store from "@/store";
import { URLResponse } from "@/utilities/types";

const BASE_URL = "http://localhost:5000/";

const arr = [
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
] as URLResponse[];

/*  user entity:
    /user/<user_id>
*/
export async function createNewUser(
  user_id: string,
  password: string,
  email: string
): Promise<boolean> {
  //   return await fetch(BASE_URL + "/user/" + store.getters.getUserId);
  return true;
}

export async function authUser(
  user_id: string,
  password: string
): Promise<boolean> {
  //   return await fetch(BASE_URL + "/get_user_urls/" + store.getters.getUserId);
  return true;
}

/*  users url entity:
    /get_user_urls/<user_id>
*/
export async function getUserUrlTranslations(): Promise<URLResponse[]> {
  //   return await fetch(BASE_URL + "/get_user_urls/" + store.getters.getUserId);
  return arr;
}

/*  translations entity:
    /translate/<short_url>
*/
export async function translateURL(short_url: string): Promise<URLResponse> {
  //   return await fetch(BASE_URL + "/get_user_urls/" + store.getters.getUserId);
  return arr[arr.findIndex((url) => url.short_url === short_url)];
}

export async function createUserTranslation(
  short_url: string,
  long_url: string
): Promise<boolean> {
  //   return await fetch(BASE_URL + "/get_user_urls/" + store.getters.getUserId);
  arr.push({
    short_url,
    long_url,
    user_id: store.getters.getUserId,
  });
  return true;
}

export async function deleteUserTranslation(
  short_url: string,
  long_url: string
): Promise<boolean> {
  //   return await fetch(BASE_URL + "/get_user_urls/" + store.getters.getUserId);
  arr.splice(
    arr.findIndex((url) => {
      return (
        url.short_url === short_url &&
        url.long_url === long_url &&
        url.user_id === store.getters.getUserId
      );
    }),
    1
  );

  return true;
}

export default {
  createNewUser,
  authUser,
  getUserUrlTranslations,
  translateURL,
  createUserTranslation,
  deleteUserTranslation,
};
