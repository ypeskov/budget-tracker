import { HttpError } from './HttpError.js';

export async function processError(e, router) {
  if (e instanceof HttpError && e.statusCode === 401) {
    console.log(e.message);
    router.push({ name: 'login' });
  } else {
    console.log(e.message);
  }
  // console.log(e);
  router.push({ name: 'home' });
}
