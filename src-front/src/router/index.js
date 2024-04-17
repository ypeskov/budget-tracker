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
      path: '/register',
      name: 'register',
      meta: {
        requiresAuth: false,
        requiresUnAuth: false,
      },
      component: () => import('../views/RegisterView.vue'),
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
    {
      path: '/transactions',
      name: 'transactions',
      meta: {
        requiresAuth: true,
        requiresUnAuth: false,
      },
      component: () => import('../views/TransactionsListView.vue'),
    },
    {
      path: '/reports',
      name: 'reports',
      meta: {
        requiresAuth: true,
        requiresUnAuth: false,
      },
      component: () => import('../views/ReportsView.vue'),
    },
    {
      path: '/reports/cashflow',
      name: 'reports-cashflow',
      meta: {
        requiresAuth: true,
        requiresUnAuth: false,
      },
      component: () => import('../views/CashFlowReportView.vue'),
    },
    {
      path: '/transactions/:id',
      name: 'transactionDetails',
      meta: {
        requiresAuth: true,
        requiresUnAuth: false,
      },
      props: route => ({
        isEdit: true,
        returnUrl: route.query.returnUrl,
        accountId: route.query.accountId, 
      }),
      component: () => import('../views/TransactionNewView.vue'),
    },
    {
      path: '/transactions/new',
      name: 'transactionNew',
      meta: {
        requiresAuth: true,
        requiresUnAuth: false,
      },
      props: route => ({ 
        returnUrl: route.query.returnUrl,
        accountId: route.query.accountId, 
      }),
      component: () => import('../views/TransactionNewView.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      meta: {
        requiresAuth: true,
        requiresUnAuth: false,
      },
      component: () => import('../views/Settings.vue'),
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
