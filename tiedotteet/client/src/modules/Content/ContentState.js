import {addToStorage, removeFromStorage} from '../../util/localStorage'

// Initial state
const initialState = {
  isFetching: false,
  error: null,
  data: []
}

// Actions
const REQUEST_CONTENT = 'CONTENT/REQUEST_CONTENT'
const requestContent = () => ({
  type: REQUEST_CONTENT
})

export const REQUEST_CONTENT_SUCCESS = 'CONTENT/REQUEST_CONTENT_SUCCESS'
const requestContentSuccess = (payload) => ({
  type: REQUEST_CONTENT_SUCCESS,
  payload
})

export const REQUEST_CONTENT_FAILURE = 'CONTENT/REQUEST_CONTENT_FAILURE'
const requestContentFailure = (payload) => ({
  type: REQUEST_CONTENT_FAILURE,
  payload
})

export const MARK_READ = 'CONTENT/MARK_READ'
export const markRead = (payload) => {
  addToStorage(payload)
  return {
    type: MARK_READ,
    payload
  }
}

export const MARK_UNREAD = 'CONTENT/MARK_UNREAD'
export const markUnRead = (payload) => {
  removeFromStorage(payload)
  return {
    type: MARK_UNREAD,
    payload
  }
}

export const fetchContent = () => {
  return (dispatch) => {
    dispatch(requestContent())
    const url = (process.env.NODE_ENV === 'production' ? '' : 'https://tiedotteet.prodeko.org') + '/api/content/'
    fetch(url, {
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": window.csrfToken,
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      method: 'get'
    }).then(response => response.json().then(json => {
      dispatch(requestContentSuccess(json))
    }))
      .catch(error => dispatch(requestContentFailure(error)))
  }
}


// Reducer
export const ContentStateReducer = (state = initialState, action = {}) => {
  switch (action.type) {
    case REQUEST_CONTENT:
      return {
        ...state,
        isFetching: true,
        error: null
      }
    case REQUEST_CONTENT_SUCCESS:
      return {
        ...state,
        isFetching: false,
        error: null,
        data: action.payload
      }
    case REQUEST_CONTENT_FAILURE:
      return {
        ...state,
        isFetching: false,
        error: action.payload
      }
    default:
      return state
  }
}
