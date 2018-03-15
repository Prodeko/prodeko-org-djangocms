import {combineReducers} from 'redux'
import {ContentStateReducer} from '../modules/Content/ContentState'

const reducer = combineReducers({
  content: ContentStateReducer
})

export default reducer
