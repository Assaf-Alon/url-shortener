import { createStore } from "vuex";

export interface MyStore {
  userID: string | null;
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
