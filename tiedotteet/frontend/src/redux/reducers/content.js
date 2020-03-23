import {
  REQUEST_CONTENT,
  REQUEST_CONTENT_SUCCESS,
  REQUEST_CONTENT_FAILURE,
} from '../actionTypes'

const initialState = {
  isFetching: false,
  error: null,
  data: [],
}

export default function ContentStateReducer(state = initialState, action = {}) {
  switch (action.type) {
    case REQUEST_CONTENT:
      return {
        ...state,
        isFetching: true,
        error: null,
      }
    case REQUEST_CONTENT_SUCCESS:
      return {
        ...state,
        isFetching: false,
        error: null,
        data: action.payload,
      }
    case REQUEST_CONTENT_FAILURE:
      return {
        ...state,
        isFetching: false,
        error: action.payload,
      }
    default:
      return state
  }
}
