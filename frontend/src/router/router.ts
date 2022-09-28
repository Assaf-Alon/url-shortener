import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import store from "@/store";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomePage.vue"),
  },
  {
    path: "/SignIn",
    name: "signIn",
    component: () => import("@/views/SignInPage.vue"),
  },
  {
    path: "/SignUp",
    name: "signUp",
    component: () => import("@/views/SignUpPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const userID = store.getters.getUserId;
  // user logged in, must go to home
  if (to.name !== "home" && userID !== null) {
    next("home");
    return;
  }
  // user not signed up, must go to signin
  if (to.name !== "signIn" && to.name !== "signUp" && userID === null) {
    next("signIn");
    return;
  }

  next();
});

export default router;
