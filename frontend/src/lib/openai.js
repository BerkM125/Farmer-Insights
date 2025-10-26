const OPENAI_API_KEY = import.meta.env.VITE_OPENAI_API_KEY;
const OPENAI_API_URL = 'https://api.openai.com/v1/responses';

export async function sendMessage(messages) {
	if (!OPENAI_API_KEY || OPENAI_API_KEY === 'your_openai_api_key_here') {
		throw new Error(
			'OpenAI API key not configured. Please set VITE_OPENAI_API_KEY in your .env file.'
		);
	}

	try {
		console.log(messages);
		const response = await fetch(OPENAI_API_URL, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${OPENAI_API_KEY}`
			},
			body: JSON.stringify({
				model: 'gpt-5-nano',
				input: messages
			})
		});

		if (!response.ok) {
			const errorData = await response.json().catch(() => ({}));
			throw new Error(
				`OpenAI API error: ${response.status} - ${errorData.error?.message || response.statusText}`
			);
		}

		const data = await response.json();
		console.log('API Response:', data);

		// Extract text from the output array
		const messageOutput = data.output?.find((item) => item.type === 'message');
		if (messageOutput?.content) {
			// Get the text from the content array
			const textContent = messageOutput.content.find((item) => item.type === 'output_text');
			return textContent?.text || 'No response received';
		}

		return 'No response received';
	} catch (error) {
		if (error.name === 'TypeError' && error.message.includes('fetch')) {
			throw new Error('Network error: Unable to connect to OpenAI API');
		}
		throw error;
	}
}
