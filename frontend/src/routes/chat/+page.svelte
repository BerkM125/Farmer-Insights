<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { sendMessageStreaming } from '$lib/api.js';

	let messages = $state([]);
	let inputValue = $state('');
	let isLoading = $state(false);
	let error = $state('');
	let streamingMessage = $state('');
	let currentStatus = $state(null);
	let inputElement;
	let messagesContainer;
	let selectedImages = $state([]);
	let fileInput;

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

	function handleImageSelect(event) {
		const files = Array.from(event.target.files || []);
		
		files.forEach(file => {
			if (!file.type.startsWith('image/')) {
				error = 'Please select only image files';
				return;
			}

			const reader = new FileReader();
			reader.onload = (e) => {
				selectedImages = [...selectedImages, {
					data: e.target.result,
					name: file.name
				}];
			};
			reader.readAsDataURL(file);
		});

		// Reset file input
		if (fileInput) {
			fileInput.value = '';
		}
	}

	function removeImage(index) {
		selectedImages = selectedImages.filter((_, i) => i !== index);
	}

	function triggerFileInput() {
		fileInput?.click();
	}

	async function handleSubmit() {
		if ((!inputValue.trim() && selectedImages.length === 0) || isLoading) return;

		const userMessage = inputValue.trim();
		const images = [...selectedImages];
		inputValue = '';
		selectedImages = [];
		isLoading = true;
		error = '';
		streamingMessage = '';
		currentStatus = null;

		// Build message content - support multimodal format if images are present
		let messageContent;
		if (images.length > 0) {
			messageContent = [
				{ type: 'text', text: userMessage || 'What do you see in this image?' }
			];
			images.forEach(img => {
				messageContent.push({
					type: 'image_url',
					image_url: { url: img.data }
				});
			});
		} else {
			messageContent = userMessage;
		}

		// Add user message
		messages = [...messages, { role: 'user', content: messageContent, images }];

		try {
			// Send all messages with streaming enabled
			const fullResponse = await sendMessageStreaming(
				messages,
				(chunk) => {
					// This callback is called for each chunk received
					streamingMessage += chunk;
					currentStatus = null; // Clear status once streaming starts
				},
				(status) => {
					// This callback is called for each status update
					currentStatus = status;
				}
			);

			// Add the complete AI response to messages
			messages = [...messages, { role: 'assistant', content: fullResponse }];
			streamingMessage = '';
			currentStatus = null;
		} catch (err) {
			error = err.message;
			streamingMessage = '';
			currentStatus = null;
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
					<div class="message-content">
						{#if message.images && message.images.length > 0}
							<div class="message-images">
								{#each message.images as image}
									<img src={image.data} alt={image.name} class="message-image" />
								{/each}
							</div>
						{/if}
						<div class="message-text">
							{#if typeof message.content === 'string'}
								{message.content}
							{:else if Array.isArray(message.content)}
								{message.content.find(item => item.type === 'text')?.text || ''}
							{/if}
						</div>
					</div>
				</div>
			{/each}

			{#if isLoading && !streamingMessage && currentStatus}
				<div class="message assistant">
					<div class="message-content loading">
						<span class="loading-icon">🔍</span>
						{currentStatus.status}
					</div>
				</div>
			{:else if isLoading && !streamingMessage}
				<div class="message assistant">
					<div class="message-content loading">
						<span class="loading-icon">✨</span>
						Thinking...
					</div>
				</div>
			{/if}

			{#if isLoading && streamingMessage}
				<div class="message assistant">
					<div class="message-content">{streamingMessage}</div>
				</div>
			{/if}

			{#if error}
				<div class="error">{error}</div>
			{/if}
		</div>

		<div class="input-area">
			<!-- Hidden file input -->
			<input
				bind:this={fileInput}
				type="file"
				accept="image/*"
				multiple
				onchange={handleImageSelect}
				style="display: none;"
			/>

			<!-- Image previews -->
			{#if selectedImages.length > 0}
				<div class="image-previews">
					{#each selectedImages as image, index}
						<div class="image-preview">
							<img src={image.data} alt={image.name} />
							<button
								class="remove-image"
								onclick={() => removeImage(index)}
								aria-label="Remove image"
							>
								×
							</button>
						</div>
					{/each}
				</div>
			{/if}

			<div class="input-row">
				<button
					class="image-button"
					onclick={triggerFileInput}
					disabled={isLoading}
					aria-label="Upload image"
					title="Upload image"
				>
					📷
				</button>
				<input
					bind:this={inputElement}
					type="text"
					bind:value={inputValue}
					onkeypress={handleKeyPress}
					placeholder="Ask a farming question..."
					disabled={isLoading}
				/>
				<button onclick={handleSubmit} disabled={isLoading || (!inputValue.trim() && selectedImages.length === 0)}> Send </button>
			</div>
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
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.loading-icon {
		display: inline-block;
		animation: gentle-pulse 1.5s ease-in-out infinite;
	}

	@keyframes gentle-pulse {
		0%,
		100% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.05);
		}
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
		flex-direction: column;
		gap: 0.5rem;
		padding-top: 0.5rem;
		border-top: 1px solid #e5e7eb;
	}

	.input-row {
		display: flex;
		gap: 0.75rem;
	}

	.image-previews {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		padding: 0.5rem;
		background: #f9fafb;
		border-radius: 8px;
	}

	.image-preview {
		position: relative;
		width: 80px;
		height: 80px;
		border-radius: 8px;
		overflow: hidden;
		border: 2px solid #e5e7eb;
	}

	.image-preview img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.remove-image {
		position: absolute;
		top: 2px;
		right: 2px;
		width: 20px;
		height: 20px;
		padding: 0;
		background: rgba(0, 0, 0, 0.6);
		color: white;
		border: none;
		border-radius: 50%;
		cursor: pointer;
		font-size: 16px;
		line-height: 1;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.remove-image:hover {
		background: rgba(0, 0, 0, 0.8);
	}

	.image-button {
		padding: 0.75rem 1rem;
		background-color: white;
		color: var(--txt-2);
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		cursor: pointer;
		font-size: 1.25rem;
		transition: all 0.2s;
	}

	.image-button:hover:not(:disabled) {
		border-color: var(--acc-1);
		background: var(--bg-2);
	}

	.image-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	input[type='text'] {
		flex: 1;
		padding: 0.75rem 1rem;
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		font-size: 1rem;
		background: white;
		color: var(--txt-1);
	}

	input[type='text']:focus {
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

	.message-images {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.message-image {
		max-width: 300px;
		max-height: 300px;
		border-radius: 8px;
		object-fit: contain;
		cursor: pointer;
	}

	.message-text {
		word-wrap: break-word;
		white-space: pre-wrap;
	}
</style>
