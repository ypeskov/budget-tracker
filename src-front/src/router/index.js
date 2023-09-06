import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '../views/HomeView.vue';
import { useUserStore } from '../stores/user';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      meta: {
        requiresAuth: false,
        requiresUnAuth: false,
      },
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      meta: {
        requiresAuth: false,
        requiresUnAuth: true,
      },
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      meta: {
        requiresAuth: false,
        requiresUnAuth: true,
      },
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/logout',
      name: 'logout',
      meta: {
        requiresAuth: false,
        requiresUnAuth: false,
      },
      component: () => import('../views/LogoutView.vue'),
    },
    {
      path: '/accounts/:id',
      name: 'accountDetails',
      meta: {
        requiresAuth: true,
        requiresUnAuth: false,
      },
      component: () => import('../views/AccountDetailsView.vue'),
    },
    {
      path: '/accounts',
      name: 'accounts',
      meta: {
        requiresAuth: true,
        requiresUnAuth: false,
      },
      component: () => import('../views/AccountsListView.vue'),
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'login' });
  } else if (to.meta.requiresUnAuth && userStore.isLoggedIn) {
    next({name: 'home'});
  } else {
    next();
  }
  
});

export default router;
