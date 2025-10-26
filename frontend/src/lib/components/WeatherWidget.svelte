<script>
	import { farmDataStore } from '$lib/stores.svelte.js';
	import { getWeatherDescription, getWeatherIcon } from '$lib/weatherHelpers.js';

	// Get today's weather (first day in forecast)
	let todayWeather = $derived(
		farmDataStore.data.weather && farmDataStore.data.weather.length > 0
			? farmDataStore.data.weather[0]
			: null
	);
</script>

<a href="/weather" class="widget weather">
	{#if todayWeather}
		{@const WeatherIcon = getWeatherIcon(todayWeather.weather_code || 0)}
		<div class="weather-main">
			<div class="weather-info">
				<div class="weather-temp">
					{Math.round(todayWeather.temperature_mean || 0)}°
				</div>
				<div class="weather-desc">{getWeatherDescription(todayWeather.weather_code || 0)}</div>
			</div>
			<div class="weather-range">
				<span class="range-label">Hi</span>
				<span class="range-value">{Math.round(todayWeather.temperature_high || 0)}°</span>
				<span class="range-label">Lo</span>
				<span class="range-value">{Math.round(todayWeather.temperature_low || 0)}°</span>
			</div>
			<WeatherIcon class="weather-icon-large" />
		</div>
		<div class="weather-stats">
			<div class="stat">
				<span class="stat-label">Humidity</span>
				<span class="stat-value"
					>{todayWeather.humidity_mean ? Math.round(todayWeather.humidity_mean) : '--'}%</span
				>
			</div>
			<div class="stat">
				<span class="stat-label">Precipitation</span>
				<span class="stat-value"
					>{todayWeather.precipitation_sum != null
						? todayWeather.precipitation_sum.toFixed(2)
						: '--'} in</span
				>
			</div>
			<div class="stat">
				<span class="stat-label">Wind</span>
				<span class="stat-value"
					>{todayWeather.wind_speed_max ? Math.round(todayWeather.wind_speed_max) : '--'} mph</span
				>
			</div>
		</div>
	{:else}
		<h2>Weather</h2>
		<p class="small-text">No data available</p>
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

	.widget.weather {
		display: flex;
		flex-direction: column;
	}

	.weather-main {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1.5rem;
		margin-bottom: 0.75rem;
	}

	.weather-temp {
		font-size: 2.5rem;
		font-weight: 600;
		line-height: 1;
		color: var(--txt-1);
	}

	.weather-desc {
		font-size: 0.875rem;
		color: var(--txt-2);
		margin-top: 0.25rem;
	}

	.weather-range {
		display: grid;
		grid-template-columns: auto auto;
		gap: 0.5rem 0.75rem;
		flex-shrink: 0;
		margin-right: auto;
		align-items: center;
	}

	.range-label {
		font-size: 1rem;
		color: var(--txt-3);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.range-value {
		font-size: 1.25rem;
		color: var(--txt-1);
		font-weight: 600;
		text-align: right;
	}

	.weather-stats {
		display: flex;
		justify-content: space-between;
		padding-top: 0.75rem;
		border-top: 1px solid var(--bg-3);
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
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--txt-1);
	}

	.small-text {
		color: var(--txt-3);
		font-size: 0.9rem;
		margin: 0;
	}

	h2 {
		font-size: 1.25rem;
		margin: 0;
	}

	:global(.weather-icon-large) {
		width: 3.75rem;
		height: 3.75rem;
		color: var(--blue-2);
		flex-shrink: 0;
	}
</style>
