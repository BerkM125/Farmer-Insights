<script>
	import { farmDataStore } from '$lib/stores.svelte.js';

	// User's crops (should match what's in +layout.svelte)
	const USER_CROPS = ['corn', 'soybeans', 'wheat'];

	// Helper function: Calculate price change percentage
	function calculatePriceChange(prices) {
		if (prices.length < 2) return null;
		const latest = prices[prices.length - 1].price;
		const previous = prices[prices.length - 2].price;
		return ((latest - previous) / previous) * 100;
	}

	// Helper function: Format unit for display
	function formatUnit(unit) {
		if (!unit) return '';
		// Convert "$ / BU" to "/bu"
		return unit.replace('$ / ', '/').toLowerCase();
	}

	// Group market data by crop
	let groupedMarketPrices = $derived(() => {
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

	// Create top market prices for home widget (limit to 2 crops)
	let topMarketPrices = $derived(() => {
		const groups = groupedMarketPrices();
		const items = [];

		// Priority order for display
		const displayCrops = ['corn', 'soybeans', 'wheat'];

		displayCrops.forEach((cropName) => {
			const prices = groups[cropName];
			if (prices && prices.length > 0) {
				const latest = prices[prices.length - 1];
				const change = calculatePriceChange(prices);

				items.push({
					name: cropName,
					displayName:
						cropName === 'soybeans' ? 'Soy' : cropName.charAt(0).toUpperCase() + cropName.slice(1),
					price: latest.price,
					unit: formatUnit(latest.unit),
					change: change,
					hasChange: change !== null
				});
			}
		});

		return items.slice(0, 2); // Show only top 2 for home widget
	});
</script>

<a href="/market" class="widget market">
	<h2>Market</h2>
	{#if topMarketPrices().length > 0}
		{#each topMarketPrices() as item}
			<div class="price-item">
				<p class="crop-name">{item.displayName}</p>
				{#if item.hasChange}
					<div class="change {item.change >= 0 ? 'up' : 'down'}">
						<span class="arrow">{item.change >= 0 ? '↑' : '↓'}</span>
						<span class="percentage">{Math.abs(item.change).toFixed(1)}%</span>
					</div>
				{:else}
					<div class="change neutral">
						<span>—</span>
					</div>
				{/if}
				<p class="price-value">${item.price.toFixed(2)}<span class="unit">{item.unit}</span></p>
			</div>
		{/each}
	{:else}
		<p class="small-text">No market data</p>
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
	}

	.widget.market {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	h2 {
		font-size: 1.25rem;
		margin: 0 0 0.25rem 0;
	}

	.price-item {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.crop-name {
		margin: 0;
		font-size: 0.875rem;
		color: var(--txt-3);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-right: auto;
	}

	.price-value {
		margin: 0;
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--txt-1);
		line-height: 1;
	}

	.unit {
		font-size: 0.875rem;
		font-weight: 400;
		color: var(--txt-3);
		margin-left: 0.125rem;
	}

	.change {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		font-size: 1rem;
		font-weight: 600;
		padding: 0.375rem 0.625rem;
		border-radius: 0.5rem;
		flex-shrink: 0;
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
		background: var(--bg-3);
		font-size: 0.875rem;
	}

	.arrow {
		font-size: 1.125rem;
		line-height: 1;
	}

	.percentage {
		line-height: 1;
	}

	.small-text {
		color: var(--txt-3);
		font-size: 0.9rem;
		margin: 0;
	}
</style>
