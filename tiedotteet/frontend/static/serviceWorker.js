const cacheName = "prodeko-tiedotteet";
const filesToCache = [];

self.addEventListener("install", e => {
  console.log("[ServiceWorker] Install");
  e.waitUntil(
    caches.open(cacheName).then(cache => {
      console.log("[ServiceWorker] Caching app shell");
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener("activate", e => {
  console.log("[ServiceWorker] Activate");
});
