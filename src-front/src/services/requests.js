/*
just a wrapper to add auth header to each request
*/

import { HttpError } from '../errors/HttpError';
import { useUserStore } from "../stores/user";

const BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST;

export async function request(endPoint, params={}, services={}) {
  const userStore = useUserStore();
  const defaultHeaders = {
    'auth-token': userStore.accessToken,
    'Content-Type': 'application/json',
  };
  const mergedHeaders = { ...defaultHeaders, ...params.headers };
  params.headers = mergedHeaders;

  const response = await fetch(`${BACKEND_HOST}${endPoint}`, params);
  
  if (response.status === 200) {
    try {
      return await response.json();
    } catch (e) {
      console.log(e);
    }
  } else if (response.status === 401) {
    services.userService.logOutUser();
    throw new HttpError('Unauthorized', 401);
  } else {
    const err = await response.json();
    console.log(err.detail);
    throw new HttpError(err.detail, response.status);
  }
  return [];
}