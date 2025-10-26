<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { sendMessageStreaming } from '$lib/api.js';

	let messages = $state([]);
	let inputValue = $state('');
	let isLoading = $state(false);
	let error = $state('');
	let streamingMessage = $state('');
	let inputElement;
	let messagesContainer;

	// Auto-focus input when page loads
	onMount(() => {
		if (inputElement) {
			inputElement.focus();
		}
	});

	// Auto-scroll to bottom when new messages arrive or streaming updates
	$effect(() => {
		// This effect runs whenever messages or streamingMessage change
		messages;
		streamingMessage;
		if (messagesContainer) {
			setTimeout(() => {
				messagesContainer.scrollTop = messagesContainer.scrollHeight;
			}, 0);
		}
	});

	async function handleSubmit() {
		if (!inputValue.trim() || isLoading) return;

		const userMessage = inputValue.trim();
		inputValue = '';
		isLoading = true;
		error = '';
		streamingMessage = '';

		// Add user message
		messages = [...messages, { role: 'user', content: userMessage }];

		try {
			// Send all messages with streaming enabled
			const fullResponse = await sendMessageStreaming(messages, (chunk) => {
				// This callback is called for each chunk received
				streamingMessage += chunk;
			});

			// Add the complete AI response to messages
			messages = [...messages, { role: 'assistant', content: fullResponse }];
			streamingMessage = '';
		} catch (err) {
			error = err.message;
			streamingMessage = '';
		} finally {
			isLoading = false;
		}
	}

	function handleKeyPress(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSubmit();
		}
	}
</script>

<div class="chat-page">
	<!-- Back Button -->
	<header>
		<button class="back-button" onclick={() => goto('/')} aria-label="Back to home">
			← Back
		</button>
		<h1>Chat with AI</h1>
	</header>

	<div class="chat-container">
		<div class="messages" bind:this={messagesContainer}>
			{#if messages.length === 0}
				<div class="empty-state">
					<p class="emoji">🌾</p>
					<p class="message">Ask me anything about farming, weather, crops, or markets!</p>
					<div class="suggestions">
						<button
							class="suggestion"
							onclick={() => (inputValue = 'What crops grow best in Iowa?')}
						>
							What crops grow best in Iowa?
						</button>
						<button
							class="suggestion"
							onclick={() => (inputValue = "What's the weather forecast for this week?")}
						>
							What's the weather forecast?
						</button>
						<button class="suggestion" onclick={() => (inputValue = 'When should I harvest corn?')}>
							When should I harvest corn?
						</button>
					</div>
				</div>
			{/if}

			{#each messages as message}
				<div class="message {message.role}">
					<div class="message-content">{message.content}</div>
				</div>
			{/each}

			{#if isLoading && streamingMessage}
				<div class="message assistant">
					<div class="message-content">{streamingMessage}</div>
				</div>
			{:else if isLoading}
				<div class="message assistant">
					<div class="message-content loading">Thinking...</div>
				</div>
			{/if}

			{#if error}
				<div class="error">{error}</div>
			{/if}
		</div>

		<div class="input-area">
			<input
				bind:this={inputElement}
				type="text"
				bind:value={inputValue}
				onkeypress={handleKeyPress}
				placeholder="Ask a farming question..."
				disabled={isLoading}
			/>
			<button onclick={handleSubmit} disabled={isLoading || !inputValue.trim()}> Send </button>
		</div>
	</div>
</div>

<style>
	.chat-page {
		display: flex;
		flex-direction: column;
		height: 100vh;
		max-width: 800px;
		margin: 0 auto;
	}

	header {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		background: white;
		border-bottom: 1px solid #e5e7eb;
	}

	header h1 {
		margin: 0;
		font-size: 1.25rem;
		color: var(--txt-1);
	}

	.back-button {
		background: none;
		border: none;
		font-size: 1rem;
		color: var(--acc-1);
		cursor: pointer;
		padding: 0.5rem;
		display: flex;
		align-items: center;
		font-weight: 600;
	}

	.back-button:hover {
		opacity: 0.8;
	}

	.chat-container {
		display: flex;
		flex-direction: column;
		flex: 1;
		padding: 1rem;
		overflow: hidden;
	}

	.messages {
		flex: 1;
		overflow-y: auto;
		margin-bottom: 1rem;
	}

	.empty-state {
		text-align: center;
		padding: 2rem 1rem;
		color: var(--txt-3);
	}

	.empty-state .emoji {
		font-size: 3rem;
		margin-bottom: 1rem;
	}

	.empty-state .message {
		font-size: 1.1rem;
		margin-bottom: 1.5rem;
	}

	.suggestions {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		max-width: 400px;
		margin: 0 auto;
	}

	.suggestion {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		padding: 0.75rem;
		cursor: pointer;
		color: var(--txt-2);
		font-size: 0.95rem;
		transition: all 0.2s;
	}

	.suggestion:hover {
		border-color: var(--acc-1);
		background: var(--bg-2);
	}

	.message {
		margin-bottom: 1rem;
	}

	.message.user {
		text-align: right;
	}

	.message.assistant {
		text-align: left;
	}

	.message-content {
		display: inline-block;
		padding: 0.75rem 1rem;
		border-radius: 12px;
		max-width: 80%;
		word-wrap: break-word;
		white-space: pre-wrap;
	}

	.message.user .message-content {
		background-color: var(--acc-1);
		color: white;
	}

	.message.assistant .message-content {
		background-color: white;
		color: var(--txt-1);
		border: 1px solid #e5e7eb;
	}

	.loading {
		font-style: italic;
		opacity: 0.7;
	}

	.error {
		background-color: #ffebee;
		color: #c62828;
		padding: 0.75rem;
		border-radius: 8px;
		margin-bottom: 1rem;
	}

	.input-area {
		display: flex;
		gap: 0.75rem;
		padding-top: 0.5rem;
		border-top: 1px solid #e5e7eb;
	}

	input {
		flex: 1;
		padding: 0.75rem 1rem;
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		font-size: 1rem;
		background: white;
		color: var(--txt-1);
	}

	input:focus {
		outline: none;
		border-color: var(--acc-1);
	}

	button {
		padding: 0.75rem 1.5rem;
		background-color: var(--acc-1);
		color: white;
		border: none;
		border-radius: 8px;
		cursor: pointer;
		font-size: 1rem;
		font-weight: 600;
		transition: background-color 0.2s;
	}

	button:hover {
		background-color: var(--acc-2);
	}

	button:disabled {
		background-color: #ccc;
		cursor: not-allowed;
	}
</style>
