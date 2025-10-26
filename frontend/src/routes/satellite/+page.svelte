<script>
	import { goto } from '$app/navigation';
</script>

<div class="page">
	<header>
		<button class="back-button" onclick={() => goto('/')} aria-label="Back to home"> ✕ </button>
		<h1>🛰️ Satellite Imagery</h1>
	</header>

	<div class="content">
		<div class="section">
			<h2>Field Overview</h2>
			<div class="map-placeholder">
				<p class="placeholder-icon">🗺️</p>
				<p class="placeholder-text">Interactive satellite map will display here</p>
				<p class="placeholder-subtext">Showing: North Field (40 acres)</p>
			</div>
		</div>

		<div class="section">
			<h2>NDVI Analysis</h2>
			<div class="ndvi-card">
				<p class="ndvi-label">Normalized Difference Vegetation Index</p>
				<p class="ndvi-value">0.72</p>
				<p class="ndvi-status good">Healthy vegetation</p>

				<div class="ndvi-legend">
					<p class="legend-title">Index Scale:</p>
					<div class="legend-bar">
						<span class="legend-label">0.0</span>
						<div class="gradient-bar"></div>
						<span class="legend-label">1.0</span>
					</div>
				</div>
			</div>
		</div>

		<div class="section">
			<h2>Historical Imagery</h2>
			<div class="timeline">
				<div class="timeline-item current">
					<p class="timeline-date">Oct 20, 2024</p>
					<div class="timeline-preview">
						<p class="preview-icon">📷</p>
						<p class="preview-label">Latest</p>
					</div>
				</div>
				<div class="timeline-item">
					<p class="timeline-date">Oct 6, 2024</p>
					<div class="timeline-preview">
						<p class="preview-icon">📷</p>
					</div>
				</div>
				<div class="timeline-item">
					<p class="timeline-date">Sep 22, 2024</p>
					<div class="timeline-preview">
						<p class="preview-icon">📷</p>
					</div>
				</div>
			</div>
		</div>

		<div class="section">
			<h2>Insights</h2>
			<div class="insight-box">
				<p class="insight-icon">✓</p>
				<div class="insight-content">
					<p class="insight-title">Uniform Growth</p>
					<p class="insight-text">
						Vegetation is growing uniformly across the field with no visible problem areas.
					</p>
				</div>
			</div>
			<div class="insight-box">
				<p class="insight-icon">💧</p>
				<div class="insight-content">
					<p class="insight-title">Moisture Variation</p>
					<p class="insight-text">
						Southwest corner shows slightly lower vegetation index, possibly indicating reduced soil
						moisture.
					</p>
				</div>
			</div>
		</div>
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

	.map-placeholder {
		background: var(--bg-2);
		border-radius: 8px;
		padding: 4rem 1rem;
		text-align: center;
	}

	.placeholder-icon {
		font-size: 3rem;
		margin: 0 0 0.5rem 0;
	}

	.placeholder-text {
		font-size: 1rem;
		color: var(--txt-2);
		margin: 0 0 0.25rem 0;
	}

	.placeholder-subtext {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0;
	}

	.ndvi-card {
		text-align: center;
		padding: 1.5rem;
		background: var(--bg-2);
		border-radius: 8px;
	}

	.ndvi-label {
		font-size: 0.9rem;
		color: var(--txt-3);
		margin: 0 0 1rem 0;
	}

	.ndvi-value {
		font-size: 3rem;
		font-weight: bold;
		color: var(--txt-1);
		margin: 0;
	}

	.ndvi-status {
		font-size: 1.1rem;
		font-weight: 600;
		margin: 0.5rem 0 1.5rem 0;
	}

	.ndvi-status.good {
		color: #10b981;
	}

	.ndvi-legend {
		max-width: 300px;
		margin: 0 auto;
	}

	.legend-title {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0 0 0.5rem 0;
		text-align: left;
	}

	.legend-bar {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.legend-label {
		font-size: 0.75rem;
		color: var(--txt-3);
	}

	.gradient-bar {
		flex: 1;
		height: 12px;
		background: linear-gradient(to right, #f87171, #fbbf24, #84cc16, #22c55e);
		border-radius: 6px;
	}

	.timeline {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0.75rem;
	}

	.timeline-item {
		text-align: center;
	}

	.timeline-item.current .timeline-preview {
		border-color: var(--acc-1);
		background: var(--bg-2);
	}

	.timeline-date {
		font-size: 0.8rem;
		color: var(--txt-3);
		margin: 0 0 0.5rem 0;
	}

	.timeline-preview {
		background: white;
		border: 2px solid #e5e7eb;
		border-radius: 8px;
		padding: 1.5rem 0.5rem;
		cursor: pointer;
		transition: all 0.2s;
	}

	.timeline-preview:hover {
		border-color: var(--acc-1);
	}

	.preview-icon {
		font-size: 2rem;
		margin: 0;
	}

	.preview-label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--acc-1);
		margin: 0.25rem 0 0 0;
	}

	.insight-box {
		display: flex;
		gap: 0.75rem;
		padding: 1rem;
		background: var(--bg-2);
		border-radius: 8px;
		margin-bottom: 0.75rem;
	}

	.insight-box:last-child {
		margin-bottom: 0;
	}

	.insight-icon {
		font-size: 1.5rem;
		margin: 0;
	}

	.insight-content {
		flex: 1;
	}

	.insight-title {
		font-weight: 600;
		color: var(--txt-1);
		margin: 0 0 0.25rem 0;
	}

	.insight-text {
		font-size: 0.9rem;
		color: var(--txt-2);
		margin: 0;
		line-height: 1.5;
	}
</style>
