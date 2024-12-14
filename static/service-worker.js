const CACHE_NAME = "recipe-app-cache-v2"; // 캐시 버전 관리
const urlsToCache = [
  "/",
  "css/style.css",
  "icons/favicon.ico",
  "icons/logo192.png",
  "icons/logo512.png",
  "templates/base.html",
  "templates/index.html",
  "templates/recipe.html"
];

// Install event
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch event
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});