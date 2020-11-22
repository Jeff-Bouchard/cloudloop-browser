import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/about",
    name: "About",
    component: () => import("../views/About.vue")
  },
  {
    path: "/sessions",
    name: "Sessions",
    component: () => import("../views/Sessions.vue")
  },
  {
    path: "/session/",
    name: "Session",
    component: () => import("../views/Session.vue")
  },
  {
    path: "/session/:sessionName",
    name: "Session",
    component: () => import("../views/Session.vue")
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue")
  },
  {
    path: "/sign-up",
    name: "SignUp",
    component: () => import("../views/SignUp.vue")
  }
];

const router = new VueRouter({
  routes
});

export default router;
