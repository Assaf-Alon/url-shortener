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
    return [];
  }
}

export async function loginAttempt(
  user_id: string,
  password: string
): Promise<boolean | string> {
  try {
    const response = await axios.get(BASE_URL + "/user/" + user_id, {
      params: {
        user_id: user_id,
        password: password,
      },
    });
    console.log(response);

    return response.data.success ? true : response.data.message;
  } catch (err) {
    console.log(err);
    if (typeof err === "object" && err !== null) {
      const message = (err as { response: { data: { message: string } } })
        .response.data.message;
      return message;
    }
    return false;
  }
}

export async function createUser(
  user_id: string,
  password: string,
  email: string
): Promise<boolean | string> {
  try {
    const response = await axios.post(BASE_URL + "/user/" + user_id, {
      user_id,
      password,
      email,
    });
    console.log(response);

    return response.status === 201 ? true : response.data.message;
  } catch (err) {
    console.log(err);
    if (typeof err === "object" && err !== null) {
      const message = (err as { message: string }).message;
      return message;
    }
    return false;
  }
}
export default { getUserUrlTranslations, loginAttempt, createUser };
