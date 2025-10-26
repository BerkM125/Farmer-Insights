<script>
	import { goto } from '$app/navigation';
	import { farmDataStore } from '$lib/stores.svelte.js';
	import BackButton from '$lib/components/BackButton.svelte';

	// User's crops (hardcoded for now, can be made dynamic later)
	const USER_CROPS = ['corn', 'soybeans', 'wheat'];

	// Helper function: Format unit for display
	function formatUnit(unit) {
		// Convert "$ / BU" to "/bushel", "$ / CWT" to "/cwt", etc.
		if (!unit) return '';
		return unit.replace('$ / ', '/').toLowerCase();
	}

	// Helper function: Calculate price change percentage
	function calculatePriceChange(prices) {
		if (prices.length < 2) return null;
		const latest = prices[prices.length - 1].price;
		const previous = prices[prices.length - 2].price;
		return ((latest - previous) / previous) * 100;
	}

	// Group market data by crop and filter for user's crops
	let groupedPrices = $derived(() => {
		const market = farmDataStore.data.market || [];
		const groups = {};

		market.forEach((item) => {
			const cropName = item.crop_name.toLowerCase();
			if (USER_CROPS.includes(cropName)) {
				if (!groups[cropName]) {
					groups[cropName] = [];
				}
				groups[cropName].push(item);
			}
		});

		// Sort each group by date
		Object.keys(groups).forEach((cropName) => {
			groups[cropName].sort((a, b) => a.date.localeCompare(b.date));
		});

		return groups;
	});

	// Create price items for display
	let priceItems = $derived(() => {
		const groups = groupedPrices();
		const items = [];

		USER_CROPS.forEach((cropName) => {
			const prices = groups[cropName];
			if (prices && prices.length > 0) {
				const latest = prices[prices.length - 1];
				const change = calculatePriceChange(prices);

				items.push({
					name: cropName,
					price: latest.price,
					unit: formatUnit(latest.unit),
					change: change,
					hasChange: change !== null
				});
			}
		});

		return items;
	});

	// Get all price data for chart (last 12 months)
	let chartData = $derived(() => {
		const groups = groupedPrices();
		const data = [];

		Object.keys(groups).forEach((cropName) => {
			const prices = groups[cropName].slice(-12); // Last 12 months
			data.push({
				crop: cropName,
				prices: prices,
				color: getCropColor(cropName)
			});
		});

		return data;
	});

	// Helper function: Get color for crop
	function getCropColor(cropName) {
		const colorMap = {
			corn: '#f59e0b',
			soybeans: '#10b981',
			wheat: '#8b5cf6'
		};
		return colorMap[cropName.toLowerCase()] || '#6b7280';
	}

	// Generate SVG path for line chart
	function generatePath(prices, width, height, minPrice, maxPrice) {
		if (prices.length === 0) return '';

		const points = prices.map((p, i) => {
			const x = (i / (prices.length - 1)) * width;
			const y = height - ((p.price - minPrice) / (maxPrice - minPrice)) * height;
			return `${x},${y}`;
		});

		return `M ${points.join(' L ')}`;
	}

	// Calculate chart bounds
	let chartBounds = $derived(() => {
		const data = chartData();
		let allPrices = [];

		data.forEach((crop) => {
			allPrices = allPrices.concat(crop.prices.map((p) => p.price));
		});

		if (allPrices.length === 0) {
			return { min: 0, max: 100 };
		}

		const min = Math.min(...allPrices);
		const max = Math.max(...allPrices);
		const padding = (max - min) * 0.1;

		return {
			min: min - padding,
			max: max + padding
		};
	});
</script>

<div class="page">
	<header>
		<BackButton href="/" label="Back to home" />
		<h1>Market Prices</h1>
		<div class="header-spacer"></div>
	</header>

	<div class="content">
		{#if farmDataStore.loading}
			<div class="loading">Loading market data...</div>
		{:else if farmDataStore.error}
			<div class="error">Error loading market data: {farmDataStore.error}</div>
		{:else if priceItems().length === 0}
			<div class="no-data">No market data available for your crops</div>
		{:else}
			<div class="section">
				<h2>Current Prices</h2>
				<div class="price-list">
					{#each priceItems() as item}
						<div class="price-item">
							<div class="price-info">
								<p class="commodity">
									{item.name.charAt(0).toUpperCase() + item.name.slice(1)}
								</p>
								<p class="price-value">
									${item.price.toFixed(2)}
									<span class="unit">{item.unit}</span>
								</p>
							</div>
							{#if item.hasChange}
								<div class="change {item.change >= 0 ? 'up' : 'down'}">
									<span class="arrow">{item.change >= 0 ? '↑' : '↓'}</span>
									<span>{Math.abs(item.change).toFixed(1)}%</span>
								</div>
							{:else}
								<div class="change neutral">
									<span>—</span>
								</div>
							{/if}
						</div>
					{/each}
				</div>
			</div>

			<div class="section">
				<h2>Price Trends (Last 12 Months)</h2>
				{#if chartData().length > 0 && chartData().some((d) => d.prices.length > 0)}
					<div class="trend-chart">
						<svg viewBox="0 0 500 250" preserveAspectRatio="xMidYMid meet">
							<!-- Grid lines -->
							<line x1="0" y1="0" x2="500" y2="0" stroke="#e5e7eb" stroke-width="1" />
							<line x1="0" y1="62.5" x2="500" y2="62.5" stroke="#e5e7eb" stroke-width="1" />
							<line x1="0" y1="125" x2="500" y2="125" stroke="#e5e7eb" stroke-width="1" />
							<line x1="0" y1="187.5" x2="500" y2="187.5" stroke="#e5e7eb" stroke-width="1" />
							<line x1="0" y1="250" x2="500" y2="250" stroke="#e5e7eb" stroke-width="1" />

							<!-- Price lines -->
							{#each chartData() as cropData}
								{#if cropData.prices.length > 1}
									<path
										d={generatePath(
											cropData.prices,
											500,
											250,
											chartBounds().min,
											chartBounds().max
										)}
										fill="none"
										stroke={cropData.color}
										stroke-width="2.5"
										stroke-linecap="round"
										stroke-linejoin="round"
									/>
								{/if}
							{/each}
						</svg>

						<!-- Legend -->
						<div class="chart-legend">
							{#each chartData() as cropData}
								{#if cropData.prices.length > 0}
									<div class="legend-item">
										<span class="legend-color" style="background-color: {cropData.color}"></span>
										<span class="legend-label">
											{cropData.crop.charAt(0).toUpperCase() + cropData.crop.slice(1)}
										</span>
									</div>
								{/if}
							{/each}
						</div>
					</div>
				{:else}
					<div class="trend-chart">
						<p class="placeholder">📊 Insufficient data for chart</p>
						<p class="chart-note">Need at least 2 months of data to display trends</p>
					</div>
				{/if}
			</div>
		{/if}
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

	.change.neutral {
		color: var(--txt-3);
		background: var(--bg-2);
		font-size: 0.9rem;
	}

	.arrow {
		font-size: 1.2rem;
	}

	.trend-chart {
		background: var(--bg-2);
		border-radius: 8px;
		padding: 1.5rem 1rem;
	}

	.trend-chart svg {
		width: 100%;
		height: auto;
		display: block;
	}

	.placeholder {
		font-size: 2rem;
		margin: 0 0 0.5rem 0;
		text-align: center;
	}

	.chart-note {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0;
		text-align: center;
	}

	.chart-legend {
		display: flex;
		justify-content: center;
		gap: 1.5rem;
		margin-top: 1rem;
		flex-wrap: wrap;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.legend-color {
		width: 16px;
		height: 16px;
		border-radius: 4px;
	}

	.legend-label {
		font-size: 0.9rem;
		color: var(--txt-2);
		font-weight: 500;
	}

	.loading,
	.error,
	.no-data {
		text-align: center;
		padding: 3rem 1rem;
		background: white;
		border-radius: 12px;
		margin: 1rem 0;
		color: var(--txt-2);
	}

	.error {
		color: #ef4444;
	}
</style>
