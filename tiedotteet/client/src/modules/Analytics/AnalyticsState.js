// Actions
const SEND_EVENT = "ANALYTICS/SEND_EVENT";
const sendEvent = (category, action, label, value) => ({
  type: SEND_EVENT,
  category,
  action,
  label,
  value
});

export const sendAnalyticsEvent = (category, action, label, value) => {
  gtag("event", "event", {
    event_category: category,
    event_action: action,
    event_label: label,
    value: value
  });
  return dispatch => {
    dispatch(sendEvent(category, action, label, value));
  };
};
