import { SEND_EVENT } from '../actionTypes'

const sendEvent = payload => ({
  type: SEND_EVENT,
  payload
})

export const sendAnalyticsEvent = payload => {
  console.log(payload)
  dataLayer.push(payload)
  return dispatch => {
    dispatch(sendEvent(payload))
  }
}
