import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import store from './redux/store'
import App from './App'
import { configureAnchors } from 'react-scrollable-anchor'
import './serviceWorker'

configureAnchors({
  offset: 0,
  scrollDuration: 0,
  keepLastAnchorHash: false,
})

render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
)
