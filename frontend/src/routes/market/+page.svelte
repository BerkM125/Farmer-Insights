<script>
	import { goto } from '$app/navigation';
	import { farmDataStore } from '$lib/stores.svelte.js';
	import BackButton from '$lib/components/BackButton.svelte';
	import MarketChart from '$lib/components/MarketChart.svelte';

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
				prices: prices
			});
		});

		return data;
	});
</script>

<div class="page">
	<header>
		<BackButton href="/" label="Back to home" />
		<h1>Market</h1>
		<div class="header-spacer"></div>
	</header>

	<div class="content">
		{#if farmDataStore.loading}
			<div class="loading">
				<div class="loading-spinner"></div>
				<p>Loading market data...</p>
			</div>
		{:else if farmDataStore.error}
			<div class="error">Error loading market data: {farmDataStore.error}</div>
		{:else if priceItems().length === 0}
			<div class="no-data">No market data available for your crops</div>
		{:else}
			<!-- Current Prices Widget -->
			<div class="widget">
				<h2>Current Prices</h2>
				<div class="price-list">
					{#each priceItems() as item}
						<div class="price-item">
							<div class="price-info">
								<span class="commodity">
									{item.name.charAt(0).toUpperCase() + item.name.slice(1)}
								</span>
								<span class="price-value">
									${item.price.toFixed(2)}
									<span class="unit">{item.unit}</span>
								</span>
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

			<!-- Price Trends Widget -->
			<div class="widget">
				<h2>Price Trends</h2>
				{#if chartData().length > 0 && chartData().some((d) => d.prices.length > 0)}
					<MarketChart chartData={chartData()} />
				{:else}
					<div class="no-chart">
						<p class="placeholder">Insufficient data for chart</p>
						<p class="chart-note">Need at least 2 months of data to display trends</p>
					</div>
				{/if}
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

	.widget {
		padding: 1rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
	}

	.widget h2 {
		margin: 0 0 1rem 0;
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	.price-list {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.price-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem;
		background: var(--bg-3);
		border-radius: 1.25rem;
		border: 1px solid var(--bg-4);
	}

	.price-info {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.commodity {
		font-size: 1rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	.price-value {
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--txt-1);
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
		border-radius: 1.5rem;
	}

	.change.up {
		color: var(--green-2);
		background: color-mix(in srgb, var(--green-1) 15%, transparent);
	}

	.change.down {
		color: var(--red-2);
		background: color-mix(in srgb, var(--red-1) 15%, transparent);
	}

	.change.neutral {
		color: var(--txt-3);
		background: var(--bg-2);
		font-size: 0.9rem;
	}

	.arrow {
		font-size: 1.2rem;
	}

	.no-chart {
		padding: 2rem 1rem;
		text-align: center;
	}

	.placeholder {
		font-size: 1.25rem;
		margin: 0 0 0.5rem 0;
		text-align: center;
		color: var(--txt-2);
	}

	.chart-note {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0;
		text-align: center;
	}

	.loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		padding: 3rem 1rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
	}

	.loading-spinner {
		width: 2rem;
		height: 2rem;
		border: 3px solid var(--bg-4);
		border-top-color: var(--txt-1);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.loading p {
		margin: 0;
		color: var(--txt-2);
	}

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
