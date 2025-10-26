<script>
	import { goto } from '$app/navigation';
	import { farmDataStore } from '$lib/stores.svelte.js';

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
		<button class="back-button" onclick={() => goto('/')} aria-label="Back to home"> ✕ </button>
		<h1>🌱 Crop Monitor</h1>
	</header>

	<div class="content">
		{#if satelliteData}
			<!-- NDVI Section -->
			<div class="section">
				<h2>Vegetation Health (NDVI)</h2>
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
						<p class="legend-desc">Red (bare/sparse) → Yellow → Green (dense vegetation)</p>
					</div>
				</div>
			</div>

			<!-- NDWI Section -->
			<div class="section">
				<h2>Water Resources (NDWI)</h2>
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
						<p class="legend-desc">Black (dry) → Blue gradient → Light blue (saturated)</p>
					</div>
				</div>
			</div>

			<!-- Insights Section -->
			{#if satelliteData.crop_advice}
				<div class="section">
					<h2>Insights & Recommendations</h2>
					<div class="insight-box">
						<p class="insight-icon">💡</p>
						<div class="insight-content">
							<p class="insight-text">{satelliteData.crop_advice}</p>
						</div>
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
	.page {
		max-width: 600px;
		margin: 0 auto;
		min-height: 100vh;
		background: var(--bg-1);
	}

	header {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		background: white;
		border-bottom: 1px solid #e5e7eb;
		position: sticky;
		top: 0;
		z-index: 10;
	}

	header h1 {
		margin: 0;
		font-size: 1.25rem;
		color: var(--txt-1);
	}

	.back-button {
		background: none;
		border: none;
		font-size: 1.5rem;
		color: var(--txt-3);
		cursor: pointer;
		padding: 0.5rem;
		display: flex;
		align-items: center;
		line-height: 1;
	}

	.back-button:hover {
		color: var(--txt-1);
	}

	.content {
		padding: 1.5rem 1rem;
	}

	.section {
		background: white;
		border-radius: 12px;
		padding: 1.25rem;
		margin-bottom: 1rem;
	}

	.section h2 {
		margin: 0 0 1rem 0;
		font-size: 1.1rem;
		color: var(--txt-2);
	}

	.map-container {
		border-radius: 8px;
		overflow: hidden;
		margin-bottom: 1rem;
		background: var(--bg-2);
	}

	.map-image {
		width: 100%;
		height: auto;
		display: block;
	}

	.map-placeholder {
		background: var(--bg-2);
		border-radius: 8px;
		padding: 3rem 1rem;
		text-align: center;
		margin-bottom: 1rem;
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
		border-radius: 8px;
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
		color: var(--yellow-1);
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
		background: linear-gradient(
			to right,
			#8b0000,
			#ff4500,
			#ffd700,
			#ffff00,
			#adff2f,
			#9acd32,
			#32cd32,
			#00ff00,
			#00cd00,
			#008000,
			#006400,
			#004000
		);
	}

	.ndwi-gradient {
		background: linear-gradient(
			to right,
			#000000,
			#0a0a1f,
			#001b4d,
			#003f7f,
			#0066b2,
			#0099cc,
			#33ccff,
			#66e0ff,
			#b3f0ff,
			#e6ffff
		);
	}

	.legend-desc {
		font-size: 0.75rem;
		color: var(--txt-3);
		margin: 0;
		font-style: italic;
	}

	.insight-box {
		display: flex;
		gap: 0.75rem;
		padding: 1rem;
		background: var(--bg-2);
		border-radius: 8px;
	}

	.insight-icon {
		font-size: 1.5rem;
		margin: 0;
	}

	.insight-content {
		flex: 1;
	}

	.insight-text {
		font-size: 0.95rem;
		color: var(--txt-2);
		margin: 0;
		line-height: 1.5;
	}

	.metadata {
		text-align: center;
		padding: 1rem;
	}

	.metadata p {
		font-size: 0.8rem;
		color: var(--txt-3);
		margin: 0.25rem 0;
	}

	.loading-state {
		text-align: center;
		padding: 3rem 1rem;
		color: var(--txt-3);
	}
</style>
