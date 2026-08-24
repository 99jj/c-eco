// c-ECO public-cache retirement worker.
// Removes previously cached technical material and then unregisters itself.
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter((name) => name.startsWith('c-eco-')).map((name) => caches.delete(name)));
    await self.clients.claim();
    const clients = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    for (const client of clients) client.postMessage({ type: 'CECO_PUBLIC_CACHE_RETIRED' });
    await self.registration.unregister();
  })());
});

self.addEventListener('fetch', () => {
  // Intentionally no interception: all requests return to the network.
});
