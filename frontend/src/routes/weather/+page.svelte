<script>
	import { goto } from '$app/navigation';
</script>

<div class="page">
	<header>
		<button class="back-button" onclick={() => goto('/')} aria-label="Back to home"> ✕ </button>
		<h1>☀️ Weather</h1>
	</header>

	<div class="content">
		<div class="current">
			<p class="big-temp">72°F</p>
			<p class="condition">Sunny</p>
			<p class="location">📍 Ames, Iowa</p>
		</div>

		<div class="section">
			<h2>7-Day Forecast</h2>
			<div class="forecast-grid">
				<div class="forecast-item">
					<p class="day">Mon</p>
					<p class="icon">☀️</p>
					<p class="temp">75°</p>
				</div>
				<div class="forecast-item">
					<p class="day">Tue</p>
					<p class="icon">🌧️</p>
					<p class="temp">68°</p>
				</div>
				<div class="forecast-item">
					<p class="day">Wed</p>
					<p class="icon">⛅</p>
					<p class="temp">70°</p>
				</div>
				<div class="forecast-item">
					<p class="day">Thu</p>
					<p class="icon">☀️</p>
					<p class="temp">73°</p>
				</div>
				<div class="forecast-item">
					<p class="day">Fri</p>
					<p class="icon">☀️</p>
					<p class="temp">76°</p>
				</div>
				<div class="forecast-item">
					<p class="day">Sat</p>
					<p class="icon">🌤️</p>
					<p class="temp">74°</p>
				</div>
				<div class="forecast-item">
					<p class="day">Sun</p>
					<p class="icon">☁️</p>
					<p class="temp">71°</p>
				</div>
			</div>
		</div>

		<div class="section">
			<h2>Details</h2>
			<div class="details-grid">
				<div class="detail-item">
					<p class="label">Humidity</p>
					<p class="value">65%</p>
				</div>
				<div class="detail-item">
					<p class="label">Wind</p>
					<p class="value">12 mph</p>
				</div>
				<div class="detail-item">
					<p class="label">Precipitation</p>
					<p class="value">20%</p>
				</div>
				<div class="detail-item">
					<p class="label">UV Index</p>
					<p class="value">7 (High)</p>
				</div>
			</div>
		</div>

		<div class="alert-box">
			<p class="alert-title">⚠️ Weather Alert</p>
			<p>Heavy rain expected tomorrow evening. Consider delaying fieldwork.</p>
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

	.alert-box {
		background: #fff3cd;
		border: 1px solid #ffc107;
		border-radius: 8px;
		padding: 1rem;
		margin-top: 1rem;
	}

	.alert-title {
		font-weight: 600;
		color: #856404;
		margin: 0 0 0.5rem 0;
	}

	.alert-box p:last-child {
		margin: 0;
		color: #856404;
	}
</style>
