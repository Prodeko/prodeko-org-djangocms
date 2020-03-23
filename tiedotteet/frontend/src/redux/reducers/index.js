import { combineReducers } from 'redux'
import ContentStateReducer from './content'

export default combineReducers({
  content: ContentStateReducer,
})
