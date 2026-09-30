const CACHE_NAME = "sr-journey-v1";

const APP_FILES = [
    "./",
    "./index.html",
    "./style.css",
    "./script.js",
    "./manifest.json"
];

// Install: save essential website files
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(APP_FILES))
            .then(() => self.skipWaiting())
    );
});

// Activate: remove older versions of this app cache
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) =>
                Promise.all(
                    keys
                        .filter((key) => key !== CACHE_NAME)
                        .map((key) => caches.delete(key))
                )
            )
            .then(() => self.clients.claim())
    );
});

// Network first; use cached files if offline
self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    const url = new URL(event.request.url);

    // Only handle requests from this website
    if (url.origin !== self.location.origin) return;

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                if (response.ok) {
                    const copy = response.clone();

                    caches.open(CACHE_NAME)
                        .then((cache) =>
                            cache.put(event.request, copy)
                        );
                }

                return response;
            })
            .catch(async () => {
                const cached = await caches.match(event.request);

                if (cached) return cached;

                if (event.request.mode === "navigate") {
                    return caches.match("./index.html");
                }

                return Response.error();
            })
    );
});