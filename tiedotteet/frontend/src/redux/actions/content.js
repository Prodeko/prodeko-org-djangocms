import {
  REQUEST_CONTENT,
  REQUEST_CONTENT_SUCCESS,
  REQUEST_CONTENT_FAILURE,
  MARK_READ,
  MARK_UNREAD,
} from '../actionTypes'
import { addToStorage, removeFromStorage } from '../../util/localStorage'

export const fetchContent = () => (dispatch) => {
  dispatch(requestContent())

  const isProd = process.env.NODE_ENV === 'production'
  const url = isProd
    ? '/tiedotteet/api/content/'
    : 'https://prodeko.org/fi/tiedotteet/api/content/'

  fetch(url, {
    method: 'get',
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': window.csrfToken,
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((json) => dispatch(requestContentSuccess(json)))
    .catch((error) => dispatch(requestContentFailure(error)))
}

export const requestContent = () => ({
  type: REQUEST_CONTENT,
})

export const requestContentSuccess = (payload) => ({
  type: REQUEST_CONTENT_SUCCESS,
  payload,
})

export const requestContentFailure = (payload) => ({
  type: REQUEST_CONTENT_FAILURE,
  payload,
})

export const markRead = (payload) => {
  addToStorage(payload)
  return {
    type: MARK_READ,
    payload,
  }
}

export const markUnRead = (payload) => {
  removeFromStorage(payload)
  return {
    type: MARK_UNREAD,
    payload,
  }
}
