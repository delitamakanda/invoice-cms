import store from '@/store'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import(/* webpackChunkName: "dashboard" */ '../views/dashboard/DashboardView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account',
    name: 'account',
    component: () => import(/* webpackChunkName: "account" */ '../views/dashboard/AccountView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account/edit-team',
    name: 'editTeam',
    component: () => import(/* webpackChunkName: "editTeam" */ '../views/dashboard/teams/EditTeamView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients',
    name: 'clients',
    component: () => import(/* webpackChunkName: "clients" */ '../views/dashboard/clients/ClientsView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/add',
    name: 'addClient',
    component: () => import(/* webpackChunkName: "addClient" */ '../views/dashboard/clients/AddClientView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/:id/edit',
    name: 'editClient',
    component: () => import(/* webpackChunkName: "editClient" */ '../views/dashboard/clients/EditClientView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/:id',
    name: 'client',
    component: () => import(/* webpackChunkName: "client" */ '../views/dashboard/clients/ClientView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices',
    name: 'invoices',
    component: () => import(/* webpackChunkName: "invoices" */ '../views/dashboard/invoices/InvoicesView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices/:id',
    name: 'invoice',
    component: () => import(/* webpackChunkName: "invoice" */ '../views/dashboard/invoices/InvoiceView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices/add',
    name: 'createInvoice',
    component: () => import(/* webpackChunkName: "createInvoice" */ '../views/dashboard/invoices/AddInvoiceView.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/sign-in',
    name: 'signin',
    component: () => import(/* webpackChunkName: "signin" */ '../views/SignInView.vue')
  },
  {
    path: '/sign-up',
    name: 'signup',
    component: () => import(/* webpackChunkName: "signup" */ '../views/SignUpView.vue')
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state['user'].isLoggedIn) {
    next('/sign-in')
  } else {
    next()
  }
})

export default router
