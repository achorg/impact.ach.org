<script>
	import { scale } from 'svelte/transition';
	/** @import { Snippet } from 'svelte' */

	/**
	 * @typedef {Object} PopupProps
	 * @prop {Snippet} [header]
	 * @prop {Snippet} content
	 * @prop {function} close
	 */

	/** @type {PopupProps} */
	let { header, content, close, ...props } = $props();
	let popup = $state();
</script>

<section transition:scale bind:this={popup} {...props}>
	{#if header}
		<header>
			{@render header()}
		</header>
	{/if}
	<div>
		{@render content()}
	</div>
	<button onclick={() => close()}>Close</button>
</section>

<svelte:window
	onclick={(e) => e.composedPath().includes(popup) || close()}
	onkeydown={({ key }) => key === 'Escape' && close()}
/>

<style>
	section {
		position: absolute;
		top: 5%;
		left: 50%;
		width: 90%;
		max-height: 90%;
		background-color: #fff;
		z-index: 1;
		border: 2px solid var(--primary-color);
		border-radius: 5px;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		max-width: 800px;
		translate: -50% 0;
		z-index: 3;
	}

	header {
		font-weight: bold;
		font-size: 1.4rem;
		background-color: var(--primary-color);
		color: #fff;
		padding: 0.5rem 1rem;
	}

	div {
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		flex-grow: 1;
		overflow-y: auto;
	}

	button {
		background-color: var(--primary-color);
		color: #fff;
		padding: 0.5rem 1rem;
		border: none;
		border-top: 1px solid var(--primary-color);
		cursor: pointer;
		transition: all 0.2s ease-in-out;

		&:hover {
			background-color: var(--secondary-color);
			border-radius: 0 0 5px 5px;
			color: var(--primary-color);
		}
	}
</style>
