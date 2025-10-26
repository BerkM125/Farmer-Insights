<script>
	import { farmDataStore } from '$lib/stores.svelte.js';

	// Get satellite data from store
	let satelliteData = $derived(farmDataStore.data.satellite);

	// Calculate status based on mean_ndvi
	let statusInfo = $derived(() => {
		if (!satelliteData || satelliteData.mean_ndvi == null) {
			return { color: 'var(--txt-3)', status: 'Pending', label: 'No data' };
		}

		const ndvi = satelliteData.mean_ndvi;
		if (ndvi > 0.7) {
			return { color: 'var(--green-1)', status: 'Healthy', label: 'Healthy crops' };
		} else if (ndvi >= 0.3) {
			return { color: 'var(--yellow-1)', status: 'Moderate', label: 'Moderate health' };
		} else {
			return { color: 'var(--red-1)', status: 'Stressed', label: 'Needs attention' };
		}
	});

	// Calculate time since update
	let timeSinceUpdate = $derived(() => {
		if (!satelliteData || !satelliteData.created_at) {
			return 'No data';
		}

		const createdAt = new Date(satelliteData.created_at);
		const now = new Date();
		const diffMs = now - createdAt;
		const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
		const diffDays = Math.floor(diffHours / 24);

		if (diffDays > 0) {
			return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
		} else if (diffHours > 0) {
			return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
		} else {
			return 'Recently';
		}
	});
</script>

<a href="/satellite" class="widget crop-monitor">
	<div class="header">
		<h2>Crop Monitor</h2>
		<div class="status-indicator" style="background-color: {statusInfo().color}"></div>
	</div>
	{#if satelliteData}
		<div class="metrics">
			<div class="metric-row">
				<span class="label">NDVI</span>
				<span class="value">{satelliteData.mean_ndvi?.toFixed(2) || 'N/A'}</span>
			</div>
			<div class="metric-row">
				<span class="label">NDWI</span>
				<span class="value">{satelliteData.mean_ndwi?.toFixed(2) || 'N/A'}</span>
			</div>
		</div>
		<!-- <p class="update-time">Updated {timeSinceUpdate()}</p> -->
	{:else}
		<p class="label">Loading...</p>
	{/if}
</a>

<style>
	.widget {
		padding: 1rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
		text-decoration: none;
		color: inherit;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.header {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	h2 {
		font-size: 1.125rem;
		margin: 0;
	}

	.status-indicator {
		width: 0.75rem;
		height: 0.75rem;
		border-radius: 50%;
		flex-shrink: 0;
	}

	.metrics {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.metric-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.label {
		font-size: 0.875rem;
		color: var(--txt-3);
	}

	.value {
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--txt-1);
	}
</style>
