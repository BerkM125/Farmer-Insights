/**
 * Global farm data store using Svelte 5 runes
 * This store manages farm data fetched from the backend API
 */

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8080';

/**
 * Create a reactive farm data store
 */
function createFarmDataStore() {
	let data = $state({
		weather: [],
		market: [],
		satellite: null,
		environmental: null
	});

	let loading = $state(false);
	let errorMsg = $state(null);

	return {
		get data() {
			return data;
		},
		get loading() {
			return loading;
		},
		get error() {
			return errorMsg;
		},
		async fetch(crops = null) {
			loading = true;
			errorMsg = null;

			try {
				// Build URL with optional crops parameter
				let url = `${BACKEND_URL}/api/farm-data`;
				if (crops && crops.length > 0) {
					const cropsParam = crops.join(',');
					url += `?crops=${encodeURIComponent(cropsParam)}`;
				}

				// Fetch farm data (weather and market)
				const response = await fetch(url);

				if (!response.ok) {
					throw new Error(`Failed to fetch farm data: ${response.statusText}`);
				}

				const result = await response.json();

				console.log('Fetched farm data:', result);
				console.log('Weather data:', result.weather);
				console.log('Market data:', result.market);

				// Update the state
				data.weather = result.weather || [];
				data.market = result.market || [];

				// Fetch satellite data separately
				const satelliteResponse = await fetch(`${BACKEND_URL}/api/satellite-data`);

				if (!satelliteResponse.ok) {
					throw new Error(`Failed to fetch satellite data: ${satelliteResponse.statusText}`);
				}

				const satelliteResult = await satelliteResponse.json();
				console.log('Fetched satellite data:', satelliteResult);

				// Update satellite data
				data.satellite = satelliteResult;

				// Fetch environmental data separately
				const environmentalResponse = await fetch(`${BACKEND_URL}/api/environmental-data`);

				if (!environmentalResponse.ok) {
					throw new Error(
						`Failed to fetch environmental data: ${environmentalResponse.statusText}`
					);
				}

				const environmentalResult = await environmentalResponse.json();
				console.log('Fetched environmental data:', environmentalResult);

				// Update environmental data
				data.environmental = environmentalResult;
			} catch (err) {
				errorMsg = err.message;
				console.error('Error fetching farm data:', err);
			} finally {
				loading = false;
			}
		}
	};
}

// Create and export a single store instance
export const farmDataStore = createFarmDataStore();
