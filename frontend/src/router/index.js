import store from '@/store'
import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/dashboard/DashboardView'

import AccountView from '@/views/dashboard/AccountView'

import EditTeamView from '@/views/dashboard/teams/EditTeamView'

import ClientsView from '@/views/dashboard/clients/ClientsView'
import AddClientView from '@/views/dashboard/clients/AddClientView'
import EditClientView from '@/views/dashboard/clients/EditClientView'
import ClientView from '@/views/dashboard/clients/ClientView'

import InvoicesView from '@/views/dashboard/invoices/InvoicesView'
import InvoiceView from '@/views/dashboard/invoices/InvoiceView'
import AddInvoiceView from '@/views/dashboard/invoices/AddInvoiceView'

import SignInView from '@/views/SignInView'
import SignUpView from '@/views/SignUpView'

import AboutView from '@/views/AboutView'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account',
    name: 'account',
    component: AccountView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account/edit-team',
    name: 'editTeam',
    component: EditTeamView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients',
    name: 'clients',
    component: ClientsView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/add',
    name: 'addClient',
    component: AddClientView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/:id/edit',
    name: 'editClient',
    component: EditClientView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/:id',
    name: 'client',
    component: ClientView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices',
    name: 'invoices',
    component: InvoicesView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices/:id',
    name: 'invoice',
    component: InvoiceView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices/add',
    name: 'createInvoice',
    component: AddInvoiceView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/sign-in',
    name: 'signin',
    component: SignInView
  },
  {
    path: '/sign-up',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.VUE_APP_BASE_URL),
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
