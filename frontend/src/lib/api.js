const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8081';

/**
 * Send a message and get a streaming response from the LLM
 * @param {Array} messages - The conversation history
 * @param {Function} onChunk - Callback function called with each text chunk
 * @param {Function} onStatus - Callback function called with status updates
 * @returns {Promise<string>} - The complete response text
 */
export async function sendMessageStreaming(messages, onChunk, onStatus) {
	try {
		console.log('Sending messages (streaming):', messages);
		console.log('Backend URL:', BACKEND_URL);
		console.log('Full URL:', `${BACKEND_URL}/rag-query`);

		const response = await fetch(`${BACKEND_URL}/rag-query`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'ngrok-skip-browser-warning': 'true'
			},
			body: JSON.stringify({
				messages: messages,
				stream: true
			})
		});

		if (!response.ok) {
			const errorData = await response.json().catch(() => ({}));
			throw new Error(
				`Backend API error: ${response.status} - ${errorData.error || response.statusText}`
			);
		}

		const reader = response.body.getReader();
		const decoder = new TextDecoder();
		let fullResponse = '';

		while (true) {
			const { done, value } = await reader.read();
			if (done) break;

			// Decode the chunk
			const chunk = decoder.decode(value, { stream: true });

			// Split by newlines to handle multiple SSE messages
			const lines = chunk.split('\n');

			for (const line of lines) {
				if (line.startsWith('data: ')) {
					const data = line.slice(6); // Remove 'data: ' prefix

					if (data === '[DONE]') {
						// Stream finished
						continue;
					}

					try {
						const parsed = JSON.parse(data);

						// Handle error messages
						if (parsed.error) {
							throw new Error(parsed.error);
						}

						// Handle status updates
						if (parsed.status) {
							if (onStatus) {
								onStatus({
									status: parsed.status,
									excerpt: parsed.excerpt,
									stage: parsed.stage
								});
							}
							continue;
						}

						// Extract the content delta from OpenAI response format
						const content = parsed.choices?.[0]?.delta?.content;
						if (content) {
							fullResponse += content;
							if (onChunk) {
								onChunk(content);
							}
						}
					} catch (e) {
						// Skip lines that aren't valid JSON (like empty lines)
						if (data.trim() && data !== '[DONE]') {
							console.error('Error parsing SSE data:', e);
						}
					}
				}
			}
		}

		return fullResponse || 'No response received';
	} catch (error) {
		console.error('API Error Details:', error);
		if (error.name === 'TypeError' && error.message.includes('fetch')) {
			throw new Error('Network error: Unable to connect to backend API');
		}
		throw error;
	}
}

/**
 * Send a message and get a non-streaming response (legacy)
 * @param {Array} messages - The conversation history
 * @returns {Promise<string>} - The complete response text
 */
export async function sendMessage(messages) {
	try {
		console.log('Sending messages:', messages);

		// Send the entire conversation history to maintain context
		const response = await fetch(`${BACKEND_URL}/rag-query`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				messages: messages
			})
		});

		if (!response.ok) {
			const errorData = await response.json().catch(() => ({}));
			throw new Error(
				`Backend API error: ${response.status} - ${errorData.error || response.statusText}`
			);
		}

		const data = await response.json();
		console.log('API Response:', data);

		// Return the RAG response
		return data.response || 'No response received';
	} catch (error) {
		if (error.name === 'TypeError' && error.message.includes('fetch')) {
			throw new Error('Network error: Unable to connect to backend API');
		}
		throw error;
	}
}
