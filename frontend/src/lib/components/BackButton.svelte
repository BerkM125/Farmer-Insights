<script>
	import { goto } from '$app/navigation';
	import PhArrowLeft from '~icons/ph/arrow-left-duotone';

	export let href = '/';
	export let label = 'Back';
</script>

<a {href} class="back-button" aria-label={label}>
	<PhArrowLeft />
</a>

<style>
	.back-button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 2.5rem;
		height: 2.5rem;
		background: var(--bg-2);
		border-radius: 50%;
		color: var(--txt-2);
		text-decoration: none;
		border: none;
		cursor: pointer;
		border: 1px solid var(--bg-3);
	}

	.back-button :global(svg) {
		width: 1.5rem;
		height: 1.5rem;
	}
</style>
