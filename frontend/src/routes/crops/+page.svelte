<script>
	import { goto } from '$app/navigation';
	import BackButton from '$lib/components/BackButton.svelte';
</script>

<div class="page">
	<header>
		<BackButton href="/" label="Back to home" />
		<h1>Your Crops</h1>
		<div class="header-spacer"></div>
	</header>

	<div class="content">
		<div class="section">
			<h2>Active Crops</h2>

			<div class="crop-card">
				<div class="crop-header">
					<p class="crop-name">🌽 Corn</p>
					<span class="status-badge flowering">Flowering</span>
				</div>
				<div class="crop-details">
					<div class="detail">
						<span class="label">Planted:</span>
						<span class="value">April 15, 2024</span>
					</div>
					<div class="detail">
						<span class="label">Field:</span>
						<span class="value">North Field (40 acres)</span>
					</div>
					<div class="detail">
						<span class="label">Est. Harvest:</span>
						<span class="value">~12 days</span>
					</div>
				</div>
				<div class="progress-bar">
					<div class="progress-fill" style="width: 75%"></div>
				</div>
				<p class="progress-label">75% to harvest</p>
			</div>

			<div class="crop-card">
				<div class="crop-header">
					<p class="crop-name">🫘 Soybeans</p>
					<span class="status-badge vegetative">Vegetative</span>
				</div>
				<div class="crop-details">
					<div class="detail">
						<span class="label">Planted:</span>
						<span class="value">May 3, 2024</span>
					</div>
					<div class="detail">
						<span class="label">Field:</span>
						<span class="value">South Field (25 acres)</span>
					</div>
					<div class="detail">
						<span class="label">Est. Harvest:</span>
						<span class="value">~35 days</span>
					</div>
				</div>
				<div class="progress-bar">
					<div class="progress-fill" style="width: 45%"></div>
				</div>
				<p class="progress-label">45% to harvest</p>
			</div>
		</div>

		<div class="section">
			<h2>Health Status</h2>
			<div class="health-grid">
				<div class="health-item good">
					<p class="health-icon">✓</p>
					<p class="health-label">Overall Health</p>
					<p class="health-value">Good</p>
				</div>
				<div class="health-item warning">
					<p class="health-icon">⚠️</p>
					<p class="health-label">Soil Moisture</p>
					<p class="health-value">Low</p>
				</div>
				<div class="health-item good">
					<p class="health-icon">✓</p>
					<p class="health-label">Pest Risk</p>
					<p class="health-value">Low</p>
				</div>
				<div class="health-item good">
					<p class="health-icon">✓</p>
					<p class="health-label">Disease Risk</p>
					<p class="health-value">Low</p>
				</div>
			</div>
		</div>

		<div class="section">
			<h2>Recommendations</h2>
			<div class="recommendation">
				<p class="rec-icon">💧</p>
				<div class="rec-content">
					<p class="rec-title">Irrigation Needed</p>
					<p class="rec-text">
						Soil moisture is below optimal levels. Consider irrigating North Field within 48 hours.
					</p>
				</div>
			</div>
			<div class="recommendation">
				<p class="rec-icon">🔍</p>
				<div class="rec-content">
					<p class="rec-title">Scout for Pests</p>
					<p class="rec-text">
						Peak season for corn borers. Conduct visual inspection in the next few days.
					</p>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
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

	.crop-card {
		background: var(--bg-2);
		border-radius: 8px;
		padding: 1rem;
		margin-bottom: 1rem;
	}

	.crop-card:last-child {
		margin-bottom: 0;
	}

	.crop-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.75rem;
	}

	.crop-name {
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--txt-1);
		margin: 0;
	}

	.status-badge {
		padding: 0.25rem 0.75rem;
		border-radius: 12px;
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
	}

	.status-badge.flowering {
		background: #fef3c7;
		color: #92400e;
	}

	.status-badge.vegetative {
		background: #d1fae5;
		color: #065f46;
	}

	.crop-details {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	.detail {
		display: flex;
		justify-content: space-between;
		font-size: 0.9rem;
	}

	.detail .label {
		color: var(--txt-3);
	}

	.detail .value {
		color: var(--txt-1);
		font-weight: 500;
	}

	.progress-bar {
		width: 100%;
		height: 8px;
		background: #e5e7eb;
		border-radius: 4px;
		overflow: hidden;
		margin-bottom: 0.5rem;
	}

	.progress-fill {
		height: 100%;
		background: var(--acc-1);
		border-radius: 4px;
		transition: width 0.3s;
	}

	.progress-label {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0;
		text-align: right;
	}

	.health-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 0.75rem;
	}

	.health-item {
		text-align: center;
		padding: 1rem;
		border-radius: 8px;
		border: 2px solid;
	}

	.health-item.good {
		background: #f0fdf4;
		border-color: #10b981;
	}

	.health-item.warning {
		background: #fffbeb;
		border-color: #f59e0b;
	}

	.health-icon {
		font-size: 1.5rem;
		margin: 0 0 0.25rem 0;
	}

	.health-label {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0 0 0.25rem 0;
	}

	.health-value {
		font-size: 1.1rem;
		font-weight: 600;
		color: var(--txt-1);
		margin: 0;
	}

	.recommendation {
		display: flex;
		gap: 0.75rem;
		padding: 1rem;
		background: var(--bg-2);
		border-radius: 8px;
		margin-bottom: 0.75rem;
	}

	.recommendation:last-child {
		margin-bottom: 0;
	}

	.rec-icon {
		font-size: 1.5rem;
		margin: 0;
	}

	.rec-content {
		flex: 1;
	}

	.rec-title {
		font-weight: 600;
		color: var(--txt-1);
		margin: 0 0 0.25rem 0;
	}

	.rec-text {
		font-size: 0.9rem;
		color: var(--txt-2);
		margin: 0;
		line-height: 1.5;
	}
</style>
