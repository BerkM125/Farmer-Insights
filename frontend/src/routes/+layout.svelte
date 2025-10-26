<script>
	import { onMount } from 'svelte';
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { farmDataStore } from '$lib/stores.svelte.js';

	let { children } = $props();

	// User's crops (hardcoded for now, could be made dynamic/configurable later)
	const USER_CROPS = ['corn', 'soybeans', 'wheat'];

	// Fetch farm data once when the app loads, filtered by user's crops
	onMount(() => {
		farmDataStore.fetch(USER_CROPS);
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children?.()}
