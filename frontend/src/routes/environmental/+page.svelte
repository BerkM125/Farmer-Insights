<script>
	import { goto } from '$app/navigation';
	import { farmDataStore } from '$lib/stores.svelte.js';
	import BackButton from '$lib/components/BackButton.svelte';

	// Get environmental data
	let envData = $derived(farmDataStore.data.environmental);

	// Helper function to determine pH status with detailed info
	function getPhStatus(ph) {
		if (!ph) return { label: 'Unknown', color: '#6b7280', advice: 'No data available' };
		if (ph < 5.5)
			return {
				label: 'Highly Acidic',
				color: '#ef4444',
				advice: 'Apply lime immediately to raise pH'
			};
		if (ph < 6.0) return { label: 'Acidic', color: '#f59e0b', advice: 'Consider applying lime' };
		if (ph > 8.0)
			return {
				label: 'Highly Alkaline',
				color: '#ef4444',
				advice: 'Apply sulfur or acidifying fertilizers'
			};
		if (ph > 7.5) return { label: 'Alkaline', color: '#f59e0b', advice: 'Monitor pH closely' };
		return { label: 'Optimal', color: '#10b981', advice: 'Maintain current levels' };
	}

	let phStatus = $derived(getPhStatus(envData?.soil_ph));

	// Generate SVG path for nitrogen levels line chart
	function generateNitrogenPath(levels, width, height) {
		if (!levels || levels.length === 0) return '';

		const min = Math.min(...levels);
		const max = Math.max(...levels);
		const range = max - min || 1;

		const points = levels.map((level, i) => {
			const x = (i / (levels.length - 1)) * width;
			const y = height - ((level - min) / range) * height;
			return `${x},${y}`;
		});

		return `M ${points.join(' L ')}`;
	}

	// Calculate nitrogen stats
	let nitrogenStats = $derived(() => {
		if (!envData?.nitrogen_levels || envData.nitrogen_levels.length === 0) {
			return { min: 0, max: 0, avg: 0, current: 0 };
		}

		const levels = envData.nitrogen_levels;
		const min = Math.min(...levels);
		const max = Math.max(...levels);
		const avg = levels.reduce((a, b) => a + b, 0) / levels.length;
		const current = levels[levels.length - 1];

		return { min, max, avg, current };
	});
</script>

<div class="page">
	<header>
		<BackButton href="/" label="Back to home" />
		<h1>Soil Monitor</h1>
		<div class="header-spacer"></div>
	</header>

	<div class="content">
		{#if farmDataStore.loading}
			<div class="loading">Loading environmental data...</div>
		{:else if farmDataStore.error}
			<div class="error">Error loading environmental data: {farmDataStore.error}</div>
		{:else if envData}
			<!-- pH Status Section -->
			<div class="section">
				<div class="status-header">
					<h2>Soil pH Status</h2>
					<span class="status-badge" style="background-color: {phStatus.color}">
						{phStatus.label}
					</span>
				</div>
				<p class="big-value">{envData.soil_ph?.toFixed(2) || '--'}</p>
				<p class="status-advice">{phStatus.advice}</p>
			</div>

			<!-- Key Metrics -->
			<div class="section">
				<h2>Key Metrics</h2>
				<div class="metrics-grid">
					<div class="metric-card">
						<p class="metric-label">Soil Temperature</p>
						<p class="metric-value">
							{envData.soil_temperature_c ? Math.round(envData.soil_temperature_c) : '--'}°C
						</p>
						<p class="metric-sublabel">
							{envData.soil_temperature_c
								? `${Math.round((envData.soil_temperature_c * 9) / 5 + 32)}°F`
								: ''}
						</p>
					</div>
					<div class="metric-card">
						<p class="metric-label">Current Nitrogen</p>
						<p class="metric-value">{nitrogenStats().current.toFixed(1)} ppm</p>
						<p class="metric-sublabel">Avg: {nitrogenStats().avg.toFixed(1)} ppm</p>
					</div>
					<div class="metric-card">
						<p class="metric-label">Sediment Level</p>
						<p class="metric-value">
							{envData.sediment_level_mg_l?.toFixed(1) || '--'} mg/L
						</p>
					</div>
					<div class="metric-card">
						<p class="metric-label">Erosion Risk</p>
						<p class="metric-value">
							{envData.erosion_risk_index != null
								? (envData.erosion_risk_index * 100).toFixed(0)
								: '--'}%
						</p>
					</div>
				</div>
			</div>

			<!-- Nitrogen Levels Chart -->
			{#if envData.nitrogen_levels && envData.nitrogen_levels.length > 0}
				<div class="section">
					<h2>Nitrogen Levels (120-Day Period)</h2>
					<div class="chart-container">
						<svg viewBox="0 0 600 200" preserveAspectRatio="xMidYMid meet">
							<!-- Grid lines -->
							<line x1="0" y1="0" x2="600" y2="0" stroke="#e5e7eb" stroke-width="1" />
							<line x1="0" y1="50" x2="600" y2="50" stroke="#e5e7eb" stroke-width="1" />
							<line x1="0" y1="100" x2="600" y2="100" stroke="#e5e7eb" stroke-width="1" />
							<line x1="0" y1="150" x2="600" y2="150" stroke="#e5e7eb" stroke-width="1" />
							<line x1="0" y1="200" x2="600" y2="200" stroke="#e5e7eb" stroke-width="1" />

							<!-- Nitrogen level line -->
							<path
								d={generateNitrogenPath(envData.nitrogen_levels, 600, 200)}
								fill="none"
								stroke="#10b981"
								stroke-width="2.5"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</svg>
						<div class="chart-info">
							<div class="info-item">
								<span class="info-label">Min:</span>
								<span class="info-value">{nitrogenStats().min.toFixed(1)} ppm</span>
							</div>
							<div class="info-item">
								<span class="info-label">Max:</span>
								<span class="info-value">{nitrogenStats().max.toFixed(1)} ppm</span>
							</div>
							<div class="info-item">
								<span class="info-label">Avg:</span>
								<span class="info-value">{nitrogenStats().avg.toFixed(1)} ppm</span>
							</div>
						</div>
					</div>
				</div>
			{/if}

			<!-- Task Recommendations -->
			{#if envData.task_recommendations && envData.task_recommendations.length > 0}
				<div class="section">
					<h2>Recommended Actions</h2>
					<div class="task-list">
						{#each envData.task_recommendations as task, i}
							<div class="task-item">
								<span class="task-number">{i + 1}</span>
								<p class="task-text">{task}</p>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Broad Advice -->
			{#if envData.broad_advice}
				<div class="section">
					<h2>Detailed Advice</h2>
					<div class="advice-content">
						{#each envData.broad_advice.split('\n') as line}
							{#if line.trim()}
								<p class="advice-line">{line}</p>
							{/if}
						{/each}
					</div>
				</div>
			{/if}

			<!-- Additional Metrics -->
			<div class="section">
				<h2>Additional Indicators</h2>
				<div class="detail-list">
					<div class="detail-row">
						<span class="detail-label">Fertilizer Availability Index</span>
						<span class="detail-value">
							{envData.fertilizer_availability_index != null
								? (envData.fertilizer_availability_index * 100).toFixed(0) + '%'
								: 'N/A'}
						</span>
					</div>
					<div class="detail-row">
						<span class="detail-label">Farm ID</span>
						<span class="detail-value">{envData.farm_id || 'N/A'}</span>
					</div>
					{#if envData.date}
						<div class="detail-row">
							<span class="detail-label">Last Updated</span>
							<span class="detail-value">{envData.date}</span>
						</div>
					{/if}
				</div>
			</div>
		{:else}
			<div class="no-data">No environmental data available</div>
		{/if}
	</div>
</div>

<style>
	.content {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.section {
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
		padding: 1rem;
	}

	.section h2 {
		margin: 0 0 1rem 0;
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	.status-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}

	.status-badge {
		color: white;
		padding: 0.375rem 0.75rem;
		border-radius: 1rem;
		font-size: 0.85rem;
		font-weight: 600;
	}

	.big-value {
		font-size: 3rem;
		font-weight: bold;
		margin: 0.5rem 0;
		color: var(--txt-1);
	}

	.status-advice {
		font-size: 1rem;
		color: var(--txt-2);
		margin: 0.5rem 0 0 0;
	}

	.metrics-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	.metric-card {
		background: var(--bg-3);
		border-radius: 1.25rem;
		border: 1px solid var(--bg-4);
		padding: 1rem;
		text-align: center;
	}

	.metric-label {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0 0 0.5rem 0;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.metric-value {
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--txt-1);
		margin: 0;
	}

	.metric-sublabel {
		font-size: 0.8rem;
		color: var(--txt-3);
		margin: 0.25rem 0 0 0;
	}

	.chart-container {
		background: var(--bg-3);
		border-radius: 1.25rem;
		border: 1px solid var(--bg-4);
		padding: 1.5rem 1rem;
	}

	.chart-container svg {
		width: 100%;
		height: auto;
		display: block;
	}

	.chart-info {
		display: flex;
		justify-content: center;
		gap: 2rem;
		margin-top: 1rem;
	}

	.info-item {
		display: flex;
		gap: 0.5rem;
		align-items: baseline;
	}

	.info-label {
		font-size: 0.85rem;
		color: var(--txt-3);
		font-weight: 500;
	}

	.info-value {
		font-size: 0.95rem;
		color: var(--txt-1);
		font-weight: 600;
	}

	.task-list {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.task-item {
		display: flex;
		gap: 0.75rem;
		align-items: flex-start;
		padding: 0.75rem;
		background: var(--bg-3);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-4);
	}

	.task-number {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 1.5rem;
		height: 1.5rem;
		background: var(--green-1);
		color: white;
		border-radius: 50%;
		font-size: 0.85rem;
		font-weight: 600;
		flex-shrink: 0;
	}

	.task-text {
		margin: 0;
		color: var(--txt-1);
		font-size: 0.95rem;
		line-height: 1.5;
		flex: 1;
	}

	.advice-content {
		background: var(--bg-3);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-4);
		padding: 1rem;
	}

	.advice-line {
		margin: 0.5rem 0;
		color: var(--txt-1);
		font-size: 0.95rem;
		line-height: 1.6;
	}

	.detail-list {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.detail-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem;
		background: var(--bg-3);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-4);
	}

	.detail-label {
		font-size: 0.95rem;
		color: var(--txt-2);
	}

	.detail-value {
		font-size: 0.95rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	.loading,
	.error,
	.no-data {
		text-align: center;
		padding: 3rem 1rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
		color: var(--txt-2);
	}

	.error {
		color: var(--red-1);
	}
</style>
