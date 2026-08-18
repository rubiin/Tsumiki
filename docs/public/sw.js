/* No-op service worker.
 *
 * This site intentionally ships no service worker. This file exists so that
 * stale registrations from previous deployments (which browsers re-fetch on
 * every navigation) resolve to a real, inert worker instead of a 404 — a 404
 * would leave the stale worker in control indefinitely.
 *
 * There is deliberately NO fetch handler here, so this worker never
 * intercepts any network request.
 */
self.addEventListener("install", function () {
  self.skipWaiting();
});

self.addEventListener("activate", function (event) {
  event.waitUntil(self.clients.claim());
});
