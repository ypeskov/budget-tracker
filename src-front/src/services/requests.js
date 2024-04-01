/*
just a wrapper to add auth header to each request
*/

import { HttpError } from '../errors/HttpError';
import { useUserStore } from "../stores/user";

const BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST;

export async function request(endPoint, params={}, services={}) {
  const userStore = useUserStore();

  let accessToken = userStore.accessToken;
  if (accessToken === null) {
    accessToken = localStorage.getItem('accessToken');
  }
  const defaultHeaders = {
    'auth-token': accessToken,
    'Content-Type': 'application/json',
  };
  const mergedHeaders = { ...defaultHeaders, ...params.headers };
  params.headers = mergedHeaders;

  const response = await fetch(`${BACKEND_HOST}${endPoint}`, params);

if ([200, 201, 204].includes(response.status)) {
  try {
    if (response.status === 204) {
      return null;
    } else {
      return await response.json();
    }
  } catch (e) {
    console.log(e);
    return null;
  }
} else {
  if (response.status === 401) {
    services.userService.logOutUser();
    throw new HttpError('Unauthorized', 401);
  } else if ([400, 500].includes(response.status)) {
    const err = await response.json();
    console.log(err.detail || 'Error occurred');
    throw new HttpError(err.detail || 'Error occurred', response.status);
  } else {
    const err = await response.json();
    console.log(err.detail || 'An unexpected error occurred');
    throw new HttpError(err.detail || 'An unexpected error occurred', response.status);
  }
}

}