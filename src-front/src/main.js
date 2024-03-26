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

const messages = {
  'en': enMessages,
  'uk': ukMessages,
}

const i18n = createI18n({
  'legacy': false,
  'locale': 'en',
  'fallbackLocale': 'en',
  'messages': messages,
})

const app = createApp(App)

app.use(createPinia());
app.use(router);
app.use(i18n);

app.mount('#app');

