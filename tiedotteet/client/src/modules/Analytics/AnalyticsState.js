

// Actions
const SEND_EVENT = 'ANALYTICS/SEND_EVENT'
const sendEvent = (category, action, label, value) => {
  return {
    type: SEND_EVENT,
    category,
    action,
    label,
    value
  }
}

export const sendAnalyticsEvent = (category, action, label, value) => {
  ga('send', {
    hitType: 'event',
    eventCategory: category,
    eventAction: action,
    eventLabel: label,
    eventValue: value
  })
  return (dispatch) => {
    dispatch(sendEvent(category, action, label, value))
  }
}
