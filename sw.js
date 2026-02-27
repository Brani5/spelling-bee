const CACHE_NAME = 'spelling-bee-v1';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async cache => {
      // Cache the main page
      await cache.add('./flashcards/index.html');
      
      // Cache all audio files by fetching the page and extracting references
      // We'll use a simpler approach: cache on first use
      return cache.addAll(['./', './flashcards/index.html']);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => 
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Cache-first strategy: serve from cache, fetch & cache if not found
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        // Cache audio and HTML files for offline use
        if (response.ok && (
          event.request.url.endsWith('.mp3') ||
          event.request.url.endsWith('.html') ||
          event.request.url.endsWith('.json') ||
          event.request.url.endsWith('.png') ||
          event.request.url.endsWith('.jpg')
        )) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      });
    })
  );
});
