/*
just a wrapper to add auth header to each request
*/

import { HttpError } from '../errors/HttpError';
import { useUserStore } from '../stores/user';

const BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST;

export async function request(endPoint, params = {}, services = {}, authRequired = true) {
  const userStore = useUserStore();

  let accessToken = userStore.accessToken;
  if (authRequired) {
    if (accessToken === null) {
      accessToken = localStorage.getItem('accessToken');
    }
    if (accessToken === null) {
      throw new HttpError('Unauthorized', 401);
    }
  }
  const defaultHeaders = {
    'auth-token': accessToken,
    'Content-Type': 'application/json',
  };
  params.headers = { ...defaultHeaders, ...params.headers };

  const response = await fetch(`${BACKEND_HOST}${endPoint}`, params);

  if ([200, 201, 204].includes(response.status)) {
    const newAccessToken = response.headers.get('new_access_token');
    if (newAccessToken) {
      userStore.accessToken = newAccessToken;
      localStorage.setItem('accessToken', newAccessToken);
    }
    try {
      if (response.status === 204) {
        return null;
      } else {
        return await response.json();
      }
    } catch (e) {
      throw new HttpError('An unexpected error occurred', response.status);
    }
  } else {
    if (response.status === 401) {
      services.userService.logOutUser();
      const body = await response.json();
      if (body.detail === 'User not activated') {
        throw new HttpError('User not activated', response.status);
      } else {
        throw new HttpError('Unauthorized', response.status);
      }
    } else if ([400, 500].includes(response.status)) {
      const err = await response.json();
      throw new HttpError(err.detail || 'An unexpected error occurred', response.status);
    } else {
      const err = await response.json();
      throw new HttpError(err.detail || 'An unexpected error occurred', response.status);
    }
  }
}