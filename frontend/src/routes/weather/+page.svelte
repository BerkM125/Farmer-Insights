<script>
	import { goto } from '$app/navigation';
	import { farmDataStore } from '$lib/stores.svelte.js';
	import {
		getWeatherDescription,
		getWeatherIcon,
		getWeatherIconColor,
		getDayOfWeek
	} from '$lib/weatherHelpers.js';
	import BackButton from '$lib/components/BackButton.svelte';

	// Get today's weather (first day in forecast)
	let today = $derived(
		farmDataStore.data.weather && farmDataStore.data.weather.length > 0
			? farmDataStore.data.weather[0]
			: null
	);

	// Track which rows are expanded (first 3 open by default)
	let expandedRows = $state([true, true, true, false, false, false, false]);

	function toggleRow(index) {
		expandedRows[index] = !expandedRows[index];
	}

	// Helper to determine field work suitability
	function getFieldCondition(day) {
		if (!day) return { status: 'Unknown', icon: '❓', color: 'var(--txt-3)' };

		const temp = day.temperature_high || day.temperature_mean || 0;
		const rain = day.precipitation_chance || 0;
		const wind = day.wind_speed_max || 0;
		const windGusts = day.wind_gusts_max || 0;

		// Check for severe conditions first
		if (temp < 32) return { status: 'Freeze Warning', icon: '●', color: 'var(--blue-1)' };
		if (rain > 70) return { status: 'Too Wet for Field Work', icon: '●', color: 'var(--red-1)' };
		if (windGusts > 25) return { status: 'Too Windy for Spraying', icon: '●', color: 'var(--yellow-1)' };

		// Check for spray conditions (50-85°F, wind < 10mph, humidity matters)
		const canSpray = temp >= 50 && temp <= 85 && wind <= 10;
		if (canSpray && rain < 30) return { status: 'Ideal for Spraying', icon: '●', color: 'var(--green-1)' };

		// General field work
		if (rain < 30 && wind < 15) return { status: 'Good for Field Work', icon: '●', color: 'var(--green-1)' };
		if (rain < 50) return { status: 'Limited Field Work', icon: '●', color: 'var(--yellow-1)' };

		return { status: 'Not Recommended', icon: '●', color: 'var(--red-1)' };
	}

	let todayCondition = $derived(getFieldCondition(today));
</script>

<div class="page">
	<header>
		<BackButton href="/" label="Back to home" />
		<h1>Weather</h1>
		<div class="header-spacer"></div>
	</header>

	<div class="content">
		{#if farmDataStore.loading}
			<div class="loading">
				<div class="loading-spinner"></div>
				<p>Loading weather data...</p>
			</div>
		{:else if farmDataStore.error}
			<div class="error">Error loading weather data: {farmDataStore.error}</div>
		{:else if today}
			<!-- 1. Current Temperature & Today's Details -->
			<div class="widget today-overview">
				<div class="current-temp">
					<p class="big-temp">{Math.round(today.temperature_high || today.temperature_mean || 0)}°F</p>
					<p class="temp-label">Today's High</p>
					<p class="location">Ames, Iowa • {getWeatherDescription(today.weather_code || 0)}</p>
				</div>

				<div class="today-details-grid">
					<div class="detail-item">
						<span class="detail-label">Rain Chance</span>
						<span class="detail-value">{today.precipitation_chance ? Math.round(today.precipitation_chance) : 0}%</span>
					</div>
					<div class="detail-item">
						<span class="detail-label">Precipitation</span>
						<span class="detail-value">{today.precipitation_sum ? today.precipitation_sum.toFixed(2) : '0.00'} in</span>
					</div>
					<div class="detail-item">
						<span class="detail-label">Wind</span>
						<span class="detail-value">{today.wind_speed_max ? Math.round(today.wind_speed_max) : 0} mph {today.wind_direction || ''}</span>
					</div>
					<div class="detail-item">
						<span class="detail-label">Humidity</span>
						<span class="detail-value">{today.humidity_mean ? Math.round(today.humidity_mean) : 'N/A'}%</span>
					</div>
					<div class="detail-item">
						<span class="detail-label">Dew Point</span>
						<span class="detail-value">{today.dew_point ? Math.round(today.dew_point) : 'N/A'}°F</span>
					</div>
					<div class="detail-item">
						<span class="detail-label">ET</span>
						<span class="detail-value">{today.evapotranspiration ? today.evapotranspiration.toFixed(2) : 'N/A'} in</span>
					</div>
				</div>
			</div>

			<!-- 2. Alerts Section (if applicable) -->
			{#if today.temperature_low < 32 || today.wind_gusts_max > 30 || today.precipitation_chance > 80}
				<div class="widget alert-section">
					<h2>Alerts</h2>
					<div class="alerts">
						{#if today.temperature_low < 32}
							<div class="alert freeze">Freeze warning: Low of {Math.round(today.temperature_low)}°F</div>
						{/if}
						{#if today.wind_gusts_max > 30}
							<div class="alert wind">High wind gusts up to {Math.round(today.wind_gusts_max)} mph</div>
						{/if}
						{#if today.precipitation_chance > 80}
							<div class="alert rain">High chance of rain ({Math.round(today.precipitation_chance)}%)</div>
						{/if}
					</div>
				</div>
			{/if}

			<!-- 3. 7-Day Detailed Forecast -->
			<div class="widget">
				<h2>7-Day Forecast</h2>
				<div class="forecast-rows">
					{#each farmDataStore.data.weather as day, index}
						{@const condition = getFieldCondition(day)}
						{@const WeatherIcon = getWeatherIcon(day.weather_code || 0)}
						{@const isExpanded = expandedRows[index]}
						<div class="forecast-row">
							<button class="row-header" onclick={() => toggleRow(index)}>
								<div class="row-left">
									<span class="row-day">{getDayOfWeek(day.date)}</span>
									<div class="row-icon">
										<WeatherIcon />
									</div>
								</div>
								<div class="row-center">
									<div class="row-temps">
										<span class="row-temp-high">{Math.round(day.temperature_high || day.temperature_mean || 0)}°</span>
										<span class="row-temp-divider">/</span>
										<span class="row-temp-low">{Math.round(day.temperature_low || day.temperature_mean || 0)}°</span>
									</div>
								</div>
								<div class="row-right">
									<span class="row-status" style="color: {condition.color}">
										{condition.icon}
									</span>
									<span class="expand-icon">{isExpanded ? '▼' : '▶'}</span>
								</div>
							</button>

							{#if isExpanded}
								<div class="row-details-expanded">
									<div class="detail-grid">
										<div class="detail-item-small">
											<span class="detail-label-small">Rain Chance</span>
											<span class="detail-value-small">{day.precipitation_chance ? Math.round(day.precipitation_chance) : 0}%</span>
										</div>
										<div class="detail-item-small">
											<span class="detail-label-small">Precipitation</span>
											<span class="detail-value-small">{day.precipitation_sum ? day.precipitation_sum.toFixed(2) : '0.00'} in</span>
										</div>
										<div class="detail-item-small">
											<span class="detail-label-small">Wind</span>
											<span class="detail-value-small">{day.wind_speed_max ? Math.round(day.wind_speed_max) : 0} mph {day.wind_direction || ''}</span>
										</div>
										<div class="detail-item-small">
											<span class="detail-label-small">Humidity</span>
											<span class="detail-value-small">{day.humidity_mean ? Math.round(day.humidity_mean) : 'N/A'}%</span>
										</div>
										<div class="detail-item-small">
											<span class="detail-label-small">Dew Point</span>
											<span class="detail-value-small">{day.dew_point ? Math.round(day.dew_point) : 'N/A'}°F</span>
										</div>
										<div class="detail-item-small">
											<span class="detail-label-small">ET</span>
											<span class="detail-value-small">{day.evapotranspiration ? day.evapotranspiration.toFixed(2) : 'N/A'} in</span>
										</div>
									</div>
									<div class="condition-badge" style="border-color: {condition.color}; color: {condition.color};">
										{condition.status}
									</div>
								</div>
							{/if}
						</div>
					{/each}
				</div>
			</div>
		{:else}
			<div class="no-data">No weather data available</div>
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

	/* Today's Overview */
	.today-overview {
		text-align: center;
	}

	.current-temp {
		padding: 1rem 0;
		border-bottom: 1px solid var(--bg-4);
		margin-bottom: 1rem;
	}

	.big-temp {
		font-size: 4rem;
		font-weight: bold;
		margin: 0;
		color: var(--txt-1);
	}

	.temp-label {
		font-size: 0.95rem;
		color: var(--txt-3);
		margin: 0.5rem 0;
	}

	.location {
		font-size: 0.9rem;
		color: var(--txt-3);
		margin: 0.5rem 0 0 0;
	}

	.today-details-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0.5rem;
	}

	.detail-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 0.75rem;
		background: var(--bg-3);
		border-radius: 1rem;
		border: 1px solid var(--bg-4);
	}

	.detail-label {
		font-size: 0.8rem;
		color: var(--txt-3);
		margin-bottom: 0.25rem;
	}

	.detail-value {
		font-size: 1.1rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	/* Alerts Section */
	.alert-section h2 {
		margin: 0 0 0.75rem 0;
	}

	.alerts {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.alert {
		padding: 0.75rem;
		background: var(--bg-3);
		border-radius: 1rem;
		border: 1px solid var(--bg-4);
		font-size: 0.95rem;
		color: var(--txt-2);
	}

	/* 7-Day Forecast Rows */
	h2 {
		margin: 0 0 1rem 0;
		font-size: 1.25rem;
		color: var(--txt-2);
	}

	.forecast-rows {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.forecast-row {
		background: var(--bg-3);
		border: 1px solid var(--bg-4);
		border-radius: 1rem;
		overflow: hidden;
	}

	.row-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.75rem;
		width: 100%;
		background: none;
		border: none;
		cursor: pointer;
		gap: 1rem;
		color: inherit;
		font-family: inherit;
		transition: background 0.2s;
	}

	.row-header:hover {
		background: var(--bg-4);
	}

	.row-left {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		min-width: 120px;
	}

	.row-day {
		font-size: 0.95rem;
		font-weight: 600;
		color: var(--txt-2);
	}

	.row-icon :global(svg) {
		width: 1.5rem;
		height: 1.5rem;
	}

	.row-center {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.row-temps {
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	.row-temp-divider {
		color: var(--txt-3);
		font-weight: normal;
		margin: 0 0.25rem;
	}

	.row-temp-low {
		color: var(--txt-3);
	}

	.row-right {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.row-status {
		font-size: 1.5rem;
	}

	.expand-icon {
		font-size: 0.75rem;
		color: var(--txt-3);
	}

	.row-details-expanded {
		padding: 0 0.75rem 0.75rem 0.75rem;
		border-top: 1px solid var(--bg-4);
	}

	.detail-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	.detail-item-small {
		display: flex;
		flex-direction: column;
		padding: 0.5rem;
		background: var(--bg-2);
		border-radius: 0.75rem;
	}

	.detail-label-small {
		font-size: 0.75rem;
		color: var(--txt-3);
		margin-bottom: 0.25rem;
	}

	.detail-value-small {
		font-size: 0.95rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	.condition-badge {
		padding: 0.5rem;
		background: var(--bg-2);
		border-radius: 0.75rem;
		text-align: center;
		font-size: 0.9rem;
		font-weight: 600;
	}

	/* Loading & Error States */
	.loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		padding: 3rem 1rem;
		color: var(--txt-2);
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

	.error,
	.no-data {
		text-align: center;
		padding: 2rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
	}

	.error {
		color: var(--red-1);
	}
</style>
