/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	// Add ngrok-skip-browser-warning header to all requests
	event.request.headers.set('ngrok-skip-browser-warning', 'true');

	return resolve(event);
}
