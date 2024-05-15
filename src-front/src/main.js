import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

import './assets/main.scss';

import { createApp } from 'vue';
import { createI18n } from 'vue-i18n'
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

import enMessages from './locales/en.json';
import ukMessages from './locales/uk.json';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: enMessages,
    uk: ukMessages,
  },
  numberFormats: {
    en: {
      currency: {
        style: 'currency',
        currency: 'USD'
      },
      decimal: {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }
    },
    uk: {
      currency: {
        style: 'currency',
        currency: 'UAH'
      },
      decimal: {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }
    },
  }
});


const app = createApp(App)

app.use(createPinia());
app.use(router);
app.use(i18n);

app.mount('#app');

