import React from 'react'
import {render} from 'react-dom'
import {Provider} from 'react-redux'
import store from './redux/store'
import App from './App'
import {configureAnchors} from 'react-scrollable-anchor'

// register service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('./static/serviceworker.js').then(function(registration) {
      // Registration was successful
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function(err) {
      // registration failed :(
      console.log('ServiceWorker registration failed: ', err);
    });
  });
}

// configure anchore-links
configureAnchors({
  offset: 0,
  scrollDuration: 0,
  keepLastAnchorHash: false
})

render(
  <Provider store={store}>
    <App/>
  </Provider>,
  document.getElementById('root')
)
