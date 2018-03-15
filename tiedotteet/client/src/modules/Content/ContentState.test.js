import { expect } from 'chai'
import {ContentStateReducer} from './ContentState'

describe('Reducer::Content', () => {
  describe('ACTION_NAME', () => {
    const initialState = {}
    const action = {}
    const nextState = ContentStateReducer(initialState, action)
    it('test case', () => {
      expect(nextState)
    })
  })
})
