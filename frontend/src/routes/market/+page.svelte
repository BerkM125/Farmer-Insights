<script>
	import { goto } from '$app/navigation';
</script>

<div class="page">
	<header>
		<button class="back-button" onclick={() => goto('/')} aria-label="Back to home"> ✕ </button>
		<h1>📈 Market Prices</h1>
	</header>

	<div class="content">
		<div class="section">
			<h2>Current Prices</h2>
			<div class="price-list">
				<div class="price-item">
					<div class="price-info">
						<p class="commodity">🌽 Corn</p>
						<p class="price-value">$4.20 <span class="unit">/bushel</span></p>
					</div>
					<div class="change up">
						<span class="arrow">↑</span>
						<span>2.4%</span>
					</div>
				</div>

				<div class="price-item">
					<div class="price-info">
						<p class="commodity">🫘 Soybeans</p>
						<p class="price-value">$12.15 <span class="unit">/bushel</span></p>
					</div>
					<div class="change down">
						<span class="arrow">↓</span>
						<span>1.2%</span>
					</div>
				</div>

				<div class="price-item">
					<div class="price-info">
						<p class="commodity">🌾 Wheat</p>
						<p class="price-value">$6.85 <span class="unit">/bushel</span></p>
					</div>
					<div class="change up">
						<span class="arrow">↑</span>
						<span>0.8%</span>
					</div>
				</div>
			</div>
		</div>

		<div class="section">
			<h2>Price Trends (30 Days)</h2>
			<div class="trend-chart">
				<p class="placeholder">📊 Chart visualization will go here</p>
				<p class="chart-note">Line chart showing corn & soy price trends over the last month</p>
			</div>
		</div>

		<div class="section">
			<h2>Market Insights</h2>
			<div class="insight-box">
				<p class="insight-icon">💡</p>
				<p class="insight-text">
					Corn prices up 2.4% this week due to strong export demand. Consider selling if prices
					reach $4.30/bushel.
				</p>
			</div>
			<div class="insight-box">
				<p class="insight-icon">📉</p>
				<p class="insight-text">
					Soybean prices declining slightly. Analysts predict stabilization next week.
				</p>
			</div>
		</div>

		<div class="section">
			<h2>Local Buyers</h2>
			<div class="buyer-list">
				<div class="buyer-item">
					<p class="buyer-name">Ames Grain Co-op</p>
					<p class="buyer-detail">📍 2.5 miles • Buying: Corn, Soy</p>
				</div>
				<div class="buyer-item">
					<p class="buyer-name">Heartland Commodities</p>
					<p class="buyer-detail">📍 8.1 miles • Buying: All grains</p>
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

	.price-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.price-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem;
		background: var(--bg-2);
		border-radius: 8px;
	}

	.commodity {
		font-size: 1.1rem;
		font-weight: 600;
		color: var(--txt-1);
		margin: 0 0 0.25rem 0;
	}

	.price-value {
		font-size: 1.5rem;
		font-weight: bold;
		color: var(--txt-1);
		margin: 0;
	}

	.unit {
		font-size: 0.85rem;
		font-weight: normal;
		color: var(--txt-3);
	}

	.change {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		font-size: 1rem;
		font-weight: 600;
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
	}

	.change.up {
		color: #10b981;
		background: #d1fae5;
	}

	.change.down {
		color: #ef4444;
		background: #fee2e2;
	}

	.arrow {
		font-size: 1.2rem;
	}

	.trend-chart {
		background: var(--bg-2);
		border-radius: 8px;
		padding: 3rem 1rem;
		text-align: center;
	}

	.placeholder {
		font-size: 2rem;
		margin: 0 0 0.5rem 0;
	}

	.chart-note {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0;
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

	.insight-text {
		flex: 1;
		margin: 0;
		color: var(--txt-2);
		line-height: 1.5;
	}

	.buyer-list {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.buyer-item {
		padding: 0.75rem;
		background: var(--bg-2);
		border-radius: 8px;
	}

	.buyer-name {
		font-weight: 600;
		color: var(--txt-1);
		margin: 0 0 0.25rem 0;
	}

	.buyer-detail {
		font-size: 0.9rem;
		color: var(--txt-3);
		margin: 0;
	}
</style>
