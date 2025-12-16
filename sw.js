// Offline cache: precache local assets, runtime-cache everything else.
// We intentionally do NOT precache CDN files to avoid cross-origin install failures.

const CACHE_STATIC = "mqk-static-v2";
const CACHE_RUNTIME = "mqk-runtime-v2";

const STATIC_ASSETS = [
  "./",
  "./index.html",
  "./style.css",
  "./app.py",
  "./manifest.json",
  "./icons/icon.svg"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE_STATIC).then((c) => c.addAll(STATIC_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(k => (k === CACHE_STATIC || k === CACHE_RUNTIME) ? null : caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  const url = new URL(req.url);

  if (req.method !== "GET") return;

  if (url.origin === location.origin) {
    // same-origin: stale-while-revalidate
    e.respondWith((async () => {
      const cache = await caches.open(CACHE_STATIC);
      const cached = await cache.match(req);
      const fetchPromise = fetch(req).then((res) => {
        cache.put(req, res.clone());
        return res;
      }).catch(() => cached);
      return cached || fetchPromise;
    })());
  } else {
    // cross-origin: runtime cache-first
    e.respondWith((async () => {
      const cache = await caches.open(CACHE_RUNTIME);
      const cached = await cache.match(req);
      if (cached) return cached;
      try {
        const res = await fetch(req);
        cache.put(req, res.clone());
        return res;
      } catch (err) {
        return cached;
      }
    })());
  }
});
