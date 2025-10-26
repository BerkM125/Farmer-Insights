<script>
	import { onMount } from 'svelte';
	import { sendMessageStreaming } from '$lib/api.js';
	import PhPlus from '~icons/ph/plus';
	import PhArrowRight from '~icons/ph/paper-plane-right-duotone';
	import PhThumbsUp from '~icons/ph/thumbs-up';
	import PhThumbsDown from '~icons/ph/thumbs-down';
	import BackButton from '$lib/components/BackButton.svelte';

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
		messages.length;
		streamingMessage.length;
		if (messagesContainer) {
			// Scroll to absolute bottom - use setTimeout to ensure DOM is fully updated
			setTimeout(() => {
				messagesContainer.scrollTop = messagesContainer.scrollHeight;
			}, 0);
		}
	});

	function handleImageSelect(event) {
		const files = Array.from(event.target.files || []);

		files.forEach((file) => {
			if (!file.type.startsWith('image/')) {
				error = 'Please select only image files';
				return;
			}

			const reader = new FileReader();
			reader.onload = (e) => {
				selectedImages = [
					...selectedImages,
					{
						data: e.target.result,
						name: file.name
					}
				];
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
		// Reset textarea height
		if (inputElement) {
			inputElement.style.height = 'auto';
		}
		isLoading = true;
		error = '';
		streamingMessage = '';
		currentStatus = null;

		// Build message content - support multimodal format if images are present
		let messageContent;
		if (images.length > 0) {
			messageContent = [{ type: 'text', text: userMessage || 'What do you see in this image?' }];
			images.forEach((img) => {
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

	function handleInput(event) {
		const textarea = event.target;
		resizeTextarea(textarea);
	}

	function resizeTextarea(textarea) {
		// Reset height to auto to get the correct scrollHeight
		textarea.style.height = 'auto';
		// Calculate number of lines
		const lineHeight = parseFloat(getComputedStyle(textarea).lineHeight);
		const lines = Math.floor(textarea.scrollHeight / lineHeight);
		// Limit to 3 rows
		if (lines <= 3) {
			textarea.style.height = textarea.scrollHeight + 'px';
			textarea.style.overflowY = 'hidden';
		} else {
			textarea.style.height = lineHeight * 3 + 'px';
			textarea.style.overflowY = 'auto';
		}
	}

	// Auto-resize textarea when inputValue changes (e.g., from suggestion buttons)
	$effect(() => {
		inputValue;
		if (inputElement) {
			setTimeout(() => resizeTextarea(inputElement), 0);
		}
	});
</script>

<div class="page">
	<!-- Back Button -->
	<header>
		<BackButton href="/" label="Back to home" />
		<h1>Chat</h1>
		<div class="header-spacer"></div>
	</header>

	<div class="chat-container">
		<div class="messages" bind:this={messagesContainer}>
			{#if messages.length === 0}
				<div class="empty-state">
					<p class="message">
						Hi there! I'm Demeter! Ask me anything about farming, weather, crops, or markets.
					</p>
					<div class="suggestions">
						<button
							class="suggestion"
							onclick={() => (inputValue = 'Should I worry about wheat rust this week?')}
						>
							Should I worry about wheat rust this week?
						</button>
						<button
							class="suggestion"
							onclick={() => (inputValue = 'Is now a good time to sell my corn?')}
						>
							Is it a good time to sell my corn?
						</button>
						<button
							class="suggestion"
							onclick={() => (inputValue = 'What should I plant based on current prices?')}
						>
							What should I plant based on current prices?
						</button>
						<button
							class="suggestion"
							onclick={() => (inputValue = 'Will the weather affect my potato harvest?')}
						>
							Will the weather affect my potato harvest?
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
								{message.content.find((item) => item.type === 'text')?.text || ''}
							{/if}
						</div>
					</div>
					{#if message.role === 'assistant'}
						<div class="feedback-buttons">
							<button class="feedback-btn" aria-label="Good response">
								<PhThumbsUp />
							</button>
							<button class="feedback-btn" aria-label="Bad response">
								<PhThumbsDown />
							</button>
						</div>
					{/if}
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
					<div class="message-content loading">Thinking...</div>
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
					<PhPlus />
				</button>
				<textarea
					bind:this={inputElement}
					bind:value={inputValue}
					onkeypress={handleKeyPress}
					oninput={handleInput}
					placeholder="Ask a farming question..."
					disabled={isLoading}
					rows="1"
				></textarea>
				<button
					class="send-button"
					onclick={handleSubmit}
					disabled={isLoading || (!inputValue.trim() && selectedImages.length === 0)}
					aria-label="Send message"
				>
					<PhArrowRight />
				</button>
			</div>
		</div>
	</div>
</div>

<style>
	.page {
		display: flex;
		flex-direction: column;
	}

	.chat-container {
		display: flex;
		flex-direction: column;
		flex: 1;
		overflow: hidden;
		gap: 0.75rem;
	}

	.messages {
		flex: 1;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.empty-state {
		text-align: center;
		padding: 2rem 1rem;
		color: var(--txt-3);
	}

	.empty-state .message {
		font-size: 1rem;
		margin-bottom: 1.5rem;
		color: var(--txt-2);
	}

	.suggestions {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		max-width: 100%;
		margin: 0 auto;
	}

	.suggestion {
		background: var(--bg-2);
		border: 1px solid var(--bg-3);
		border-radius: 1.75rem;
		padding: 0.75rem 1rem;
		cursor: pointer;
		color: var(--txt-2);
		font-size: 0.95rem;
		transition: all 0.2s;
	}

	.suggestion:hover {
		background: var(--bg-3);
		border-color: var(--bg-4);
	}

	.message {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.message.user {
		align-items: flex-end;
	}

	.message.assistant {
		align-items: flex-start;
	}

	.message-content {
		padding: 0.75rem 1rem;
		border-radius: 1.75rem;
		max-width: 85%;
		word-wrap: break-word;
	}

	.message.user .message-content {
		background-color: var(--green-1);
		color: var(--txt-1);
	}

	.message.assistant .message-content {
		background-color: var(--bg-2);
		color: var(--txt-1);
		border: 1px solid var(--bg-3);
	}

	.loading {
		font-style: italic;
		opacity: 0.8;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		color: var(--txt-2);
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
		background-color: var(--red-1);
		color: var(--txt-1);
		padding: 0.75rem 1rem;
		border-radius: 1.75rem;
		margin-bottom: 0.5rem;
		text-align: center;
	}

	.input-area {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.input-row {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		background: var(--bg-3);
		border-radius: 1.75rem;
		padding: 0.5rem;
		border: 1px solid var(--bg-4);
	}

	.image-previews {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		padding: 0.5rem;
		background: var(--bg-2);
		border-radius: 1.75rem;
		border: 1px solid var(--bg-3);
	}

	.image-preview {
		position: relative;
		width: 70px;
		height: 70px;
		border-radius: 1.25rem;
		overflow: hidden;
		border: 2px solid var(--bg-4);
	}

	.image-preview img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.remove-image {
		position: absolute;
		top: 4px;
		right: 4px;
		width: 20px;
		height: 20px;
		padding: 0;
		background: rgba(0, 0, 0, 0.7);
		color: white;
		border: none;
		border-radius: 50%;
		cursor: pointer;
		font-size: 14px;
		line-height: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: bold;
	}

	.remove-image:hover {
		background: rgba(0, 0, 0, 0.9);
	}

	.image-button {
		padding: 0.5rem;
		background-color: var(--bg-2);
		color: var(--txt-1);
		border: 1px solid var(--bg-4);
		border-radius: 50%;
		cursor: pointer;
		transition: all 0.2s;
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

	.image-button:hover:not(:disabled) {
		background: var(--bg-4);
	}

	.image-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	textarea {
		flex: 1;
		padding: 0.5rem 0;
		border: none;
		background: transparent;
		font-size: 1rem;
		color: var(--txt-1);
		min-width: 0;
		resize: none;
		font-family: inherit;
		line-height: 1.5;
		overflow-y: hidden;
		max-height: calc(1.5em * 3);
	}

	textarea:focus {
		outline: none;
	}

	textarea::placeholder {
		color: var(--txt-3);
	}

	.send-button {
		padding: 0.5rem;
		background-color: var(--green-1);
		color: var(--txt-1);
		border: none;
		border-radius: 50%;
		cursor: pointer;
		transition: all 0.2s;
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

	.send-button:hover:not(:disabled) {
		background-color: var(--green-2);
	}

	.send-button:disabled {
		background-color: var(--bg-4);
		color: var(--txt-3);
		cursor: not-allowed;
	}

	.message-images {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.message-image {
		max-width: 100%;
		max-height: 250px;
		border-radius: 1rem;
		object-fit: contain;
		cursor: pointer;
	}

	.message-text {
		word-wrap: break-word;
		white-space: pre-wrap;
	}

	.feedback-buttons {
		display: flex;
		gap: 0.25rem;
		margin-left: 0.5rem;
	}

	.feedback-btn {
		background: transparent;
		border: none;
		color: var(--txt-3);
		cursor: pointer;
		padding: 0.25rem;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: color 0.2s;
	}

	.feedback-btn :global(svg) {
		width: 0.875rem;
		height: 0.875rem;
	}

	.feedback-btn:hover {
		color: var(--txt-2);
	}
</style>
