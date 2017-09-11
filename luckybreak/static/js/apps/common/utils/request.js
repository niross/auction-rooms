/**
 * Helper functions to be used when making requests to the api.
 */
import JsCookie from 'js-cookie';

/**
 * Check the response status and raise an error if it's no good.
 * @param {object} response - the http response object as provided by fetch
 * @returns {object} - the http rsponse object or throws an error
 */
export function checkStatus(response) {
  if (response.ok) {
    return response;
  }
  return response.json().then(json => {
    const error = new Error(response.statusText);
    throw Object.assign(error, { response, json });
  });
}

/**
 * Return an object given an http json response
 * @param {object} response - json encoded response object as provided by fetch
 * @returns {object} - The parsed json
 */
export function parseJSON(response) {
  return response.json();
}


/**
 * Return the headers needed for put, post and delete requests
 * @returns {{Accept: string, Content-Type: string, X-CSRFToken: *}}
 */
export function getRequestHeaders(form = false) {
  let contentType = 'application/json';
  if (form) contentType = 'application/x-www-form-urlencoded; charset=utf-8';
  const headers = {
    Accept: 'application/json, application/json, application/coreapi+json',
    'Content-Type': contentType
  };
  const csrf = JsCookie.get('csrftoken');
  if (csrf) headers['X-CSRFToken'] = csrf;
  return headers;
}

/**
 * Make a GET request, check and parse the response
 */
export function makeApiCall(url, method = 'GET', data = null) {
  const options = {
    method,
    credentials: 'include',
    headers: getRequestHeaders()
  };
  if (data !== null) {
    options.body = JSON.stringify(data);
  }
  return fetch(url, options)
    .then(checkStatus)
    .then(parseJSON);
}

// export function makeRequest(url, method = 'GET', body = {}, formEncoded = false, json = true) {
//   const resp = fetch(url, {
//     method,
//     body,
//     credentials: 'include',
//     headers: getRequestHeaders(formEncoded)
//   })
//     .then(checkStatus);
//   if (json) {
//     return resp.then(parseJSON);
//   }
//   return resp;
// }
