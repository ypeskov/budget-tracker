/*
just a wrapper to add auth header to each request
*/

import { useUserStore } from "../stores/user";

const BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST;

export async function request(endPoint, params={}) {
  const userStore = useUserStore();
  const defaultHeaders = {
    'auth-token': userStore.accessToken,
    'Content-Type': 'application/json',
  };
  const mergedHeaders = { ...defaultHeaders, ...params.headers };
  params.headers = mergedHeaders;

  return await fetch(`${BACKEND_HOST}${endPoint}`, params);
}