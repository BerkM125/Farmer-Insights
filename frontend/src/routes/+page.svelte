<script>
	import { goto } from '$app/navigation';
</script>

<div class="home">
	<header>
		<h1>🌾 Farmer Insights</h1>
		<p class="location">📍 Ames, Iowa</p>
	</header>

	<!-- Widget Grid -->
	<div class="widgets">
		<button class="widget weather" onclick={() => goto('/weather')}>
			<div class="widget-header">
				<h2>☀️ Weather</h2>
				<span class="arrow">→</span>
			</div>
			<p class="big-text">72°F</p>
			<p class="small-text">Sunny</p>
			<p class="alert">⚠️ Rain tomorrow</p>
		</button>

		<button class="widget market" onclick={() => goto('/market')}>
			<div class="widget-header">
				<h2>📈 Market Prices</h2>
				<span class="arrow">→</span>
			</div>
			<p class="price">Corn: $4.20/bu <span class="change up">↑2%</span></p>
			<p class="price">Soy: $12.15/bu <span class="change down">↓1%</span></p>
		</button>

		<button class="widget crops" onclick={() => goto('/crops')}>
			<div class="widget-header">
				<h2>🌱 Your Crops</h2>
				<span class="arrow">→</span>
			</div>
			<p>Corn - Stage: Flowering</p>
			<p>Estimated harvest: ~12 days</p>
		</button>

		<button class="widget satellite" onclick={() => goto('/satellite')}>
			<div class="widget-header">
				<h2>🛰️ Field Imagery</h2>
				<span class="arrow">→</span>
			</div>
			<p>Last updated: 2 days ago</p>
			<p class="small-text">Tap to view NDVI analysis</p>
		</button>
	</div>

	<!-- Chat Bar (navigates to chat) -->
	<button class="chat-bar" onclick={() => goto('/chat')}>
		<span class="chat-icon">💬</span>
		<span class="chat-placeholder">Ask AI anything about your farm...</span>
	</button>
</div>

<style>
	.home {
		max-width: 600px;
		margin: 0 auto;
		padding: 1rem;
		padding-bottom: 2rem;
	}

	header {
		text-align: center;
		margin-bottom: 2rem;
	}

	header h1 {
		margin: 0;
		font-size: 1.75rem;
		color: var(--txt-1);
	}

	.location {
		margin: 0.5rem 0 0 0;
		color: var(--txt-3);
		font-size: 0.95rem;
	}

	.widgets {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.widget {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 12px;
		padding: 1.25rem;
		text-align: left;
		cursor: pointer;
		transition: all 0.2s;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.widget:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
	}

	.widget:active {
		transform: translateY(0);
	}

	.widget-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.75rem;
	}

	.widget h2 {
		margin: 0;
		font-size: 1.1rem;
		color: var(--txt-2);
	}

	.arrow {
		font-size: 1.5rem;
		color: var(--acc-1);
		opacity: 0.6;
	}

	.widget p {
		margin: 0.5rem 0 0 0;
		color: var(--txt-2);
	}

	.big-text {
		font-size: 2.5rem;
		font-weight: bold;
		color: var(--txt-1);
		margin: 0.5rem 0;
	}

	.small-text {
		font-size: 0.9rem;
		color: var(--txt-3);
	}

	.alert {
		color: #e67700;
		font-weight: 500;
		margin-top: 0.75rem !important;
	}

	.price {
		font-size: 1rem;
		margin: 0.5rem 0;
	}

	.change {
		font-size: 0.85rem;
		font-weight: 600;
	}

	.change.up {
		color: #10b981;
	}

	.change.down {
		color: #ef4444;
	}

	/* Chat Bar */
	.chat-bar {
		position: fixed;
		bottom: 1rem;
		left: 1rem;
		right: 1rem;
		max-width: 580px;
		margin: 0 auto;
		background: white;
		border: 2px solid var(--acc-1);
		border-radius: 50px;
		padding: 1rem 1.5rem;
		display: flex;
		align-items: center;
		gap: 1rem;
		cursor: pointer;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		transition: all 0.2s;
	}

	.chat-bar:hover {
		transform: translateY(-2px);
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
	}

	.chat-icon {
		font-size: 1.5rem;
	}

	.chat-placeholder {
		flex: 1;
		text-align: left;
		color: var(--txt-3);
		font-size: 1rem;
	}
</style>
