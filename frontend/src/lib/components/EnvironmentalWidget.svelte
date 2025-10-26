<script>
	import { farmDataStore } from '$lib/stores.svelte.js';

	// Get environmental data
	let environmentalData = $derived(farmDataStore.data.environmental);

	// Helper function to determine pH status
	function getPhStatus(ph) {
		if (!ph) return { label: 'Unknown', color: 'var(--txt-3)' };
		if (ph < 5.5) return { label: 'Highly Acidic', color: 'var(--red-1)' };
		if (ph < 6.0) return { label: 'Acidic', color: 'var(--yellow-1)' };
		if (ph > 8.0) return { label: 'Highly Alkaline', color: 'var(--red-1)' };
		if (ph > 7.5) return { label: 'Alkaline', color: 'var(--yellow-1)' };
		return { label: 'Optimal', color: 'var(--green-1)' };
	}

	let phStatus = $derived(getPhStatus(environmentalData?.soil_ph));
</script>

<a href="/environmental" class="widget environmental">
	<div class="header">
		<h2>Soil Monitor</h2>
		<div class="status-indicator" style="background-color: {phStatus.color}"></div>
	</div>
	{#if environmentalData}
		<div class="metrics">
			<div class="metric-row">
				<span class="label">pH</span>
				<span class="value">{environmentalData.soil_ph?.toFixed(1) || '--'}</span>
			</div>
			<div class="metric-row">
				<span class="label">Temp</span>
				<span class="value"
					>{environmentalData.soil_temperature_c
						? Math.round(environmentalData.soil_temperature_c)
						: '--'}°C</span
				>
			</div>
		</div>
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
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.value {
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--txt-1);
	}
</style>
