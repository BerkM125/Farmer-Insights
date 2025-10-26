<script>
	import { goto } from '$app/navigation';
	import { farmDataStore } from '$lib/stores.svelte.js';
	import BackButton from '$lib/components/BackButton.svelte';

	// Get satellite data from store
	let satelliteData = $derived(farmDataStore.data.satellite);

	// Calculate time since update
	function getTimeSinceUpdate(createdAt) {
		if (!createdAt) return 'Unknown';

		const created = new Date(createdAt);
		const now = new Date();
		const diffMs = now - created;
		const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
		const diffDays = Math.floor(diffHours / 24);

		if (diffDays > 0) {
			return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
		} else if (diffHours > 0) {
			return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
		} else {
			return 'Recently';
		}
	}

	// Format number to 3 decimal places
	function formatStat(value) {
		if (value == null) return 'N/A';
		return value.toFixed(3);
	}

	// Get status text based on NDVI
	function getNDVIStatus(mean) {
		if (mean == null) return { text: 'Unknown', class: 'neutral' };
		if (mean > 0.7) return { text: 'Healthy vegetation', class: 'good' };
		if (mean >= 0.3) return { text: 'Moderate vegetation', class: 'moderate' };
		return { text: 'Stressed vegetation', class: 'poor' };
	}

	// Get status text based on NDWI
	function getNDWIStatus(mean) {
		if (mean == null) return { text: 'Unknown', class: 'neutral' };
		if (mean > 0.5) return { text: 'High water content', class: 'good' };
		if (mean > 0.1) return { text: 'Adequate water content', class: 'moderate' };
		return { text: 'Low water content', class: 'poor' };
	}
</script>

<div class="page">
	<header>
		<BackButton href="/" label="Back to home" />
		<h1>Crop Monitor</h1>
		<div class="header-spacer"></div>
	</header>

	<div class="content">
		{#if satelliteData}
			<!-- NDVI Section -->
			{#if satelliteData.ndvi_url}
				<div class="map-container">
					<img src={satelliteData.ndvi_url} alt="NDVI Vegetation Map" class="map-image" />
				</div>
			{:else}
				<div class="map-placeholder">
					<p class="placeholder-icon">🗺️</p>
					<p class="placeholder-text">NDVI map not available</p>
				</div>
			{/if}

			<div class="stats-card">
				<h2>Vegetation Health (NDVI)</h2>
				{#if satelliteData.mean_ndvi != null}
					{@const status = getNDVIStatus(satelliteData.mean_ndvi)}
					<p class="status-label">Status</p>
					<p class="status-value {status.class}">{status.text}</p>
				{:else}
					<p class="status-label">Status</p>
					<p class="status-value neutral">Unknown</p>
				{/if}

				<div class="stats-grid">
					<div class="stat">
						<span class="stat-label">Mean</span>
						<span class="stat-value">{formatStat(satelliteData.mean_ndvi)}</span>
					</div>
					<div class="stat">
						<span class="stat-label">Median</span>
						<span class="stat-value">{formatStat(satelliteData.median_ndvi)}</span>
					</div>
					<div class="stat">
						<span class="stat-label">25th percentile</span>
						<span class="stat-value">{formatStat(satelliteData['25th_ndvi'])}</span>
					</div>
					<div class="stat">
						<span class="stat-label">75th percentile</span>
						<span class="stat-value">{formatStat(satelliteData['75th_ndvi'])}</span>
					</div>
				</div>

				<div class="legend">
					<p class="legend-title">NDVI Scale:</p>
					<div class="legend-bar">
						<span class="legend-label">-0.2</span>
						<div class="gradient-bar ndvi-gradient"></div>
						<span class="legend-label">1.0</span>
					</div>
					<p class="legend-desc">Red (poor) → Yellow → Green → Teal (very healthy)</p>
				</div>
			</div>

			<!-- NDWI Section -->
			{#if satelliteData.ndwi_url}
				<div class="map-container">
					<img src={satelliteData.ndwi_url} alt="NDWI Water Resources Map" class="map-image" />
				</div>
			{:else}
				<div class="map-placeholder">
					<p class="placeholder-icon">🗺️</p>
					<p class="placeholder-text">NDWI map not available</p>
				</div>
			{/if}

			<div class="stats-card">
				<h2>Water Resources (NDWI)</h2>
				{#if satelliteData.mean_ndwi != null}
					{@const status = getNDWIStatus(satelliteData.mean_ndwi)}
					<p class="status-label">Status</p>
					<p class="status-value {status.class}">{status.text}</p>
				{:else}
					<p class="status-label">Status</p>
					<p class="status-value neutral">Unknown</p>
				{/if}

				<div class="stats-grid">
					<div class="stat">
						<span class="stat-label">Mean</span>
						<span class="stat-value">{formatStat(satelliteData.mean_ndwi)}</span>
					</div>
					<div class="stat">
						<span class="stat-label">Median</span>
						<span class="stat-value">{formatStat(satelliteData.median_ndwi)}</span>
					</div>
					<div class="stat">
						<span class="stat-label">25th percentile</span>
						<span class="stat-value">{formatStat(satelliteData['25th_ndwi'])}</span>
					</div>
					<div class="stat">
						<span class="stat-label">75th percentile</span>
						<span class="stat-value">{formatStat(satelliteData['75th_ndwi'])}</span>
					</div>
				</div>

				<div class="legend">
					<p class="legend-title">NDWI Scale:</p>
					<div class="legend-bar">
						<span class="legend-label">-1.0</span>
						<div class="gradient-bar ndwi-gradient"></div>
						<span class="legend-label">1.0</span>
					</div>
					<p class="legend-desc">Black (dry) → Teal (saturated)</p>
				</div>
			</div>

			<!-- Insights Section -->
			{#if satelliteData.crop_advice}
				<div class="insight-box">
					<h2>Recommendations</h2>
					<div class="insight-content">
						<p class="insight-text">{satelliteData.crop_advice}</p>
					</div>
				</div>
			{/if}

			<!-- Metadata -->
			<div class="metadata">
				<p>Last updated: {getTimeSinceUpdate(satelliteData.created_at)}</p>
				<p>
					Location: {satelliteData.latitude?.toFixed(4)}°N, {satelliteData.longitude?.toFixed(4)}°W
				</p>
			</div>
		{:else}
			<div class="loading-state">
				<p>Loading satellite data...</p>
			</div>
		{/if}
	</div>
</div>

<style>
	.content {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.stats-card h2,
	.insight-box h2 {
		margin: 0 0 1rem 0;
		font-size: 1.25rem;
		color: var(--txt-1);
	}

	.map-container {
		border-radius: 1.75rem;
		overflow: hidden;
		background: var(--bg-2);
		border: 1px solid var(--bg-3);
	}

	.map-image {
		width: 100%;
		height: auto;
		display: block;
	}

	.map-placeholder {
		background: var(--bg-3);
		border-radius: 1.75rem;
		padding: 3rem 1rem;
		text-align: center;
	}

	.placeholder-icon {
		font-size: 3rem;
		margin: 0 0 0.5rem 0;
	}

	.placeholder-text {
		font-size: 1rem;
		color: var(--txt-2);
		margin: 0;
	}

	.stats-card {
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
		padding: 1rem;
	}

	.status-label {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0 0 0.25rem 0;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.status-value {
		font-size: 1.25rem;
		font-weight: 600;
		margin: 0 0 1rem 0;
	}

	.status-value.good {
		color: var(--green-2);
	}

	.status-value.moderate {
		color: var(--yellow-2);
	}

	.status-value.poor {
		color: var(--red-2);
	}

	.status-value.neutral {
		color: var(--txt-3);
	}

	.stats-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1rem;
		margin-bottom: 1rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid var(--bg-3);
	}

	.stat {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.stat-label {
		font-size: 0.75rem;
		color: var(--txt-3);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.stat-value {
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	.legend {
		margin-top: 1rem;
	}

	.legend-title {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0 0 0.5rem 0;
	}

	.legend-bar {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.legend-label {
		font-size: 0.75rem;
		color: var(--txt-3);
		font-weight: 600;
	}

	.gradient-bar {
		flex: 1;
		height: 12px;
		border-radius: 6px;
	}

	.ndvi-gradient {
		background: linear-gradient(to right, #e06c6c, #dbba57, #97c639, var(--blue-1));
	}

	.ndwi-gradient {
		background: linear-gradient(to right, #000000, var(--blue-1));
	}

	.legend-desc {
		font-size: 0.75rem;
		color: var(--txt-3);
		margin: 0;
		font-style: italic;
	}

	.insight-box {
		padding: 1rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
	}

	.insight-header {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	.insight-icon {
		font-size: 1.5rem;
		margin: 0;
	}

	.insight-content {
	}

	.insight-text {
		line-height: 1.5;
	}

	.metadata {
		padding: 1rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
		flex-direction: column;
		display: flex;
		gap: 0.5rem;
	}

	.metadata p {
		font-size: 0.75rem;
		color: var(--txt-3);
		margin: 0;
	}

	.loading-state {
		text-align: center;
		padding: 3rem 1rem;
		color: var(--txt-3);
	}
</style>
