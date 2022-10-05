import { createStore } from "vuex";
import { userID } from "@/utilities/types";

export interface MyStore {
  userID: userID;
}

export default createStore({
  state: {
    userID: null,
  } as MyStore,
  getters: {
    getUserId(state) {
      return state.userID;
    },
  },
  mutations: {
    setUserId(state, newUserId) {
      state.userID = newUserId;
    },
  },
  actions: {
    setUserId({ commit }, userID) {
      commit("setUserId", userID);
    },
  },
});
