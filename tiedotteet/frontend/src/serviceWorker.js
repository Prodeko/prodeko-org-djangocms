if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./assets/serviceworker.js').then(
      (registration) => {
        console.log(
          'ServiceWorker registration successful with scope: ',
          registration.scope
        )
      },
      (err) => {
        console.log('ServiceWorker registration failed: ', err)
      }
    )
  })
}
