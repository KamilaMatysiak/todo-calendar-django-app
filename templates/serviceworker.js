var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
     '/offline/',
    // '/css/django-pwa-app.css',
    '/static/image/icon-192.png',
    '/static/image/icon-512.png',
    '/static/image/push-icon.png',
    '/static/image/app-icon.png',
    '/static/image/favicon.png'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {

    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
/* self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('offline');
            })
    )
}); */
self.addEventListener("fetch", event => {
    event.respondWith(fetch(event.request)
        .then(res=>{console.log(res); return res;})
    .catch(err=>{console.error(err);return err;}));
});






self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || '';
    const body = data.body || '';

    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: '/static/image/push-icon.png'
        })
    );
});

