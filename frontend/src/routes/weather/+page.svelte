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
</script>

<div class="page">
	<header>
		<BackButton href="/" label="Back to home" />
		<h1>Weather</h1>
		<div class="header-spacer"></div>
	</header>

	<div class="content">
		{#if farmDataStore.loading}
			<div class="loading">Loading weather data...</div>
		{:else if farmDataStore.error}
			<div class="error">Error loading weather data: {farmDataStore.error}</div>
		{:else if today}
			<div class="current">
				<p class="big-temp">
					{Math.round(today.temperature_high || today.temperature_mean || 0)}°F
				</p>
				<p class="condition">{getWeatherDescription(today.weather_code || 0)}</p>
				<p class="location">📍 Ames, Iowa</p>
			</div>

			<div class="section">
				<h2>7-Day Forecast</h2>
				<div class="forecast-grid">
					{#each farmDataStore.data.weather as day}
						{@const WeatherIcon = getWeatherIcon(day.weather_code || 0)}
						{@const iconColor = getWeatherIconColor(day.weather_code || 0)}
						<div class="forecast-item">
							<p class="day">{getDayOfWeek(day.date)}</p>
							<div class="icon">
								<WeatherIcon style="color: {iconColor}" />
							</div>
							<p class="temp">{Math.round(day.temperature_high || day.temperature_mean || 0)}°</p>
						</div>
					{/each}
				</div>
			</div>

			<div class="section">
				<h2>Today's Details</h2>
				<div class="details-grid">
					<div class="detail-item">
						<p class="label">Humidity</p>
						<p class="value">{today.humidity_mean ? Math.round(today.humidity_mean) : 'N/A'}%</p>
					</div>
					<div class="detail-item">
						<p class="label">Wind</p>
						<p class="value">
							{today.wind_speed_max ? Math.round(today.wind_speed_max) : 'N/A'} mph
							{today.wind_direction || ''}
						</p>
					</div>
					<div class="detail-item">
						<p class="label">Precipitation</p>
						<p class="value">
							{today.precipitation_chance ? Math.round(today.precipitation_chance) : 'N/A'}%
						</p>
					</div>
					<div class="detail-item">
						<p class="label">Rain Amount</p>
						<p class="value">
							{today.precipitation_sum ? today.precipitation_sum.toFixed(2) : 'N/A'} in
						</p>
					</div>
				</div>
			</div>

			<div class="section">
				<h2>All Weather Data (Debug)</h2>
				<pre>{JSON.stringify(farmDataStore.data.weather, null, 2)}</pre>
			</div>
		{:else}
			<div class="no-data">No weather data available</div>
		{/if}
	</div>
</div>

<style>
	.content {
		padding: 1.5rem 1rem;
	}

	.current {
		text-align: center;
		padding: 2rem 0;
		background: white;
		border-radius: 12px;
		margin-bottom: 1.5rem;
	}

	.big-temp {
		font-size: 4rem;
		font-weight: bold;
		margin: 0;
		color: var(--txt-1);
	}

	.condition {
		font-size: 1.5rem;
		margin: 0.5rem 0;
		color: var(--txt-2);
	}

	.location {
		font-size: 1rem;
		color: var(--txt-3);
		margin: 0.5rem 0 0 0;
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

	.forecast-grid {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: 0.5rem;
	}

	.forecast-item {
		text-align: center;
	}

	.forecast-item .day {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0 0 0.25rem 0;
	}

	.forecast-item .icon {
		font-size: 1.5rem;
		margin: 0.25rem 0;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.forecast-item .icon :global(svg) {
		width: 1.5rem;
		height: 1.5rem;
	}

	.forecast-item .temp {
		font-size: 0.9rem;
		font-weight: 600;
		color: var(--txt-2);
		margin: 0.25rem 0 0 0;
	}

	.details-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	.detail-item {
		text-align: center;
		padding: 0.75rem;
		background: var(--bg-2);
		border-radius: 8px;
	}

	.detail-item .label {
		font-size: 0.85rem;
		color: var(--txt-3);
		margin: 0 0 0.25rem 0;
	}

	.detail-item .value {
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--txt-1);
		margin: 0;
	}

	.loading,
	.error,
	.no-data {
		text-align: center;
		padding: 2rem;
		background: white;
		border-radius: 12px;
		margin: 1rem 0;
	}

	.error {
		color: var(--red-1);
	}

	pre {
		background: var(--bg-2);
		padding: 1rem;
		border-radius: 8px;
		overflow-x: auto;
		font-size: 0.75rem;
		line-height: 1.4;
	}
</style>
