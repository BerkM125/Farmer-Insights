const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8080';

export async function sendMessage(messages) {
	try {
		console.log('Sending messages:', messages);

		// Extract the user's question from messages
		const userMessage = messages.find(m => m.role === 'user')?.content || messages[messages.length - 1]?.content;

		const response = await fetch(`${BACKEND_URL}/rag-query`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				prompt: userMessage
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
