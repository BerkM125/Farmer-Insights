<script>
	// No need for goto since we're using links
</script>

<div class="container">
	<header>
		<h1>Demeter</h1>
		<p class="location">Ames, Iowa</p>
	</header>

	<!-- Widget Grid -->
	<div class="widgets">
		<a href="/weather" class="widget weather">
			<h2>Weather</h2>
			<p class="big-text">72°F</p>
			<p class="small-text">Sunny</p>
			<p class="alert">Rain tomorrow</p>
		</a>

		<a href="/market" class="widget market">
			<h2>Market Prices</h2>
			<p class="price">Corn: $4.20/bu <span class="change up">↑2%</span></p>
			<p class="price">Soy: $12.15/bu <span class="change down">↓1%</span></p>
		</a>

		<a href="/satellite" class="widget satellite">
			<h2>Field Imagery</h2>
			<p>Last updated: 2 days ago</p>
			<p class="small-text">Tap to view NDVI analysis</p>
		</a>

		<a href="/crops" class="widget crops">
			<h2>Environment</h2>
			<p>Corn - Stage: Flowering</p>
			<p>Estimated harvest: ~12 days</p>
		</a>
	</div>

	<!-- Chat Bar (navigates to chat) -->
	<a href="/chat" class="chat-bar">
		<span class="chat-icon"></span>
		<span class="chat-placeholder">Ask anything...</span>
	</a>
</div>

<style>
	.container {
		max-width: 35rem;
		margin: 0 auto;
		padding: 0.75rem;
		min-height: 100vh;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	header {
	}

	header h1 {
		margin: 0;
	}

	.widgets {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.75rem;
		margin-bottom: 3rem;
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

	.widget p {
		margin: 0.5rem 0 0 0;
	}

	.chat-bar {
		padding: 1rem;
		background: var(--bg-3);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-4);
		cursor: text;
	}

	.chat-placeholder {
		color: var(--txt-3);
	}
</style>
