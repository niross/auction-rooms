/**
 * Helper functions to be used when making requests to the api.
 */
import JsCookie from 'js-cookie';
import 'isomorphic-fetch';


/**
 * Parse a django rest framework error response into easier to
 * handle javascript object
 *
 * from {name: ['this field is required']} to {name: 'this field is required'}
 */
function parseErrors(errorFields) {
  const errors = {};
  Object.keys(errorFields).forEach((key) => {
    const value = errorFields[key];
    if (value.constructor === Array) {
      if (value.length > 0) {
        errors[key] = value[0];
      }
    }
    else {
      errors[key] = value;
    }
  });
  return errors;
}


/**
 * Check the response status and raise an error if it's no good.
 * @param {object} response - the http response object as provided by fetch
 * @returns {object} - the http rsponse object or throws an error
 */
export function checkStatus(response) {
  if (response.ok) {
    return response;
  }
  return response.json().then((json) => {
    const error = new Error(response.statusText);
    throw Object.assign(error, { fieldErrors: parseErrors(json), response, json });
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
export function getRequestHeaders(contentType) {
  const headers = {
    Accept: 'application/json, application/json, application/coreapi+json'
  };
  if (contentType) headers['Content-Type'] = contentType;
  const csrf = JsCookie.get('csrftoken');
  if (csrf) headers['X-CSRFToken'] = csrf;
  return headers;
}

export function makeApiCall(url, method, data, json = true, contentType = 'application/json') {
  const response = fetch(url, {
    method,
    headers: getRequestHeaders(contentType),
    credentials: 'include',
    body: contentType === 'application/json' ? JSON.stringify(data) : data
  })
    .then(checkStatus);

  return json ? response.then(parseJSON) : response;
}

