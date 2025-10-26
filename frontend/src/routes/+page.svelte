<script>
	import { farmDataStore } from '$lib/stores.svelte.js';
	import WeatherWidget from '$lib/components/WeatherWidget.svelte';
	import MarketWidget from '$lib/components/MarketWidget.svelte';
	import CropMonitorWidget from '$lib/components/CropMonitorWidget.svelte';
	import EnvironmentalWidget from '$lib/components/EnvironmentalWidget.svelte';
	import PhPlus from '~icons/ph/plus';
	import PhArrowRight from '~icons/ph/paper-plane-right-duotone';
</script>

<div class="container">
	<header>
		<div class="title-section">
			<h1>Demeter</h1>
			<div class="accent-boxes">
				<div class="accent-box red"></div>
				<div class="accent-box yellow"></div>
				<div class="accent-box green"></div>
				<div class="accent-box blue"></div>
			</div>
		</div>
		<!-- <p class="location">Ames, Iowa</p> -->
	</header>

	<!-- Widget Grid -->
	{#if farmDataStore.loading}
		<div class="widgets-loading">
			<div class="loading-spinner"></div>
			<p class="loading-text">Loading farm data...</p>
		</div>
	{:else if farmDataStore.error}
		<div class="widgets-error">
			<p class="error-text">Error loading data: {farmDataStore.error}</p>
		</div>
	{:else}
		<div class="widgets">
			<WeatherWidget />

			<MarketWidget />

			<div class="side-by-side">
				<CropMonitorWidget />

				<EnvironmentalWidget />
			</div>

			<div class="widget action-items">
				<h2>Action Items</h2>
				<div class="action-list">
					<div class="action-item">
						<span>Fertilize corn field</span>
					</div>
					<div class="action-item">
						<span>Check irrigation system</span>
					</div>
					<div class="action-item">
						<span>Review market trends</span>
					</div>
				</div>
			</div>
		</div>
	{/if}

	<!-- Chat Bar (navigates to chat) -->
	<a href="/chat" class="chat-bar">
		<span class="image-button">
			<PhPlus />
		</span>
		<span class="chat-placeholder">Ask a farming question...</span>
		<span class="send-button">
			<PhArrowRight />
		</span>
	</a>
</div>

<style>
	.container {
		max-width: 35rem;
		margin: 0 auto;
		padding: 1rem 0.75rem;
		min-height: 100vh;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.title-section {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	h1 {
		margin: 0;
		letter-spacing: -2%;
	}

	.accent-boxes {
		display: flex;
		transform: skewX(-15deg);
	}

	.accent-box {
		width: 1rem;
		height: 2rem;
	}

	.accent-box.red {
		background: var(--red-1);
	}

	.accent-box.yellow {
		background: var(--yellow-1);
	}

	.accent-box.green {
		background: var(--green-1);
	}

	.accent-box.blue {
		background: var(--blue-1);
	}

	.widgets {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.widgets-loading,
	.widgets-error {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		padding: 3rem 1rem;
	}

	.loading-text {
		color: var(--txt-2);
		font-size: 1rem;
		margin: 0;
	}

	.widgets-error .error-text {
		color: var(--red-1);
		margin: 0;
	}

	.side-by-side {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.5rem;
	}

	.action-list {
		margin-top: 0.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.action-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem;
		background: var(--bg-3);
		border-radius: 1.25rem;
		border: 1px solid var(--bg-4);
	}

	.widget {
		padding: 1rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
	}

	h2 {
		font-size: 1.25rem;
		margin: 0;
	}

	.chat-bar {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		background: var(--bg-3);
		border-radius: 1.75rem;
		padding: 0.5rem;
		border: 1px solid var(--bg-4);
		cursor: text;
	}

	.image-button {
		padding: 0.5rem;
		background-color: var(--bg-2);
		color: var(--txt-1);
		border: 1px solid var(--bg-4);
		border-radius: 50%;
		width: 2.5rem;
		height: 2.5rem;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.image-button :global(svg) {
		width: 1.25rem;
		height: 1.25rem;
	}

	.chat-placeholder {
		color: var(--txt-3);
		flex: 1;
		padding: 0.5rem 0;
		font-size: 1rem;
		min-width: 0;
	}

	.send-button {
		padding: 0.5rem;
		background-color: var(--green-1);
		color: var(--txt-1);
		border-radius: 50%;
		width: 2.5rem;
		height: 2.5rem;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.send-button :global(svg) {
		width: 1.25rem;
		height: 1.25rem;
	}

	.loading-spinner {
		width: 2rem;
		height: 2rem;
		border: 3px solid var(--bg-4);
		border-top-color: var(--txt-1);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0.5rem 0;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.error-text {
		color: var(--red-1);
		font-size: 0.875rem;
	}
</style>
