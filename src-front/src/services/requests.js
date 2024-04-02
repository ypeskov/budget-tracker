/*
just a wrapper to add auth header to each request
*/

import { useRouter } from 'vue-router';
import { HttpError } from '../errors/HttpError';
import { useUserStore } from '../stores/user';
import { processError } from '../errors/errorHandlers';

const BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST;

export async function request(endPoint, params = {}, services = {}) {
  const userStore = useUserStore();
  const router = useRouter();

  let accessToken = userStore.accessToken;
  if (accessToken === null) {
    accessToken = localStorage.getItem('accessToken');
  }
  const defaultHeaders = {
    'auth-token': accessToken,
    'Content-Type': 'application/json',
  };
  params.headers = { ...defaultHeaders, ...params.headers };

  const response = await fetch(`${BACKEND_HOST}${endPoint}`, params);

  if ([200, 201, 204].includes(response.status)) {
    try {
      if (response.status === 204) {
        return null;
      } else {
        return await response.json();
      }
    } catch (e) {
      await processError(e, router);
    }
  } else {
    if (response.status === 401) {
      services.userService.logOutUser();
      await processError(new HttpError('Unauthorized', response.status), router);
    } else if ([400, 500].includes(response.status)) {
      const err = await response.json();
      await processError(new HttpError(err.detail || 'An unexpected error occurred', response.status), router);
    } else {
      const err = await response.json();
      await processError(new HttpError(err.detail || 'An unexpected error occurred', response.status), router);
    }
  }
}