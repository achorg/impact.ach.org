<script>
	import { scale } from 'svelte/transition';
	/** @import { Item } from '$components/Table.svelte' */

	/**
	 * @typedef {Object} DetailsProps
	 * @prop {Item} item
	 * @prop {function} close
	 */

	/** @type {DetailsProps} */
	let { item, close, ...props } = $props();
	let details = $state();
</script>

<section transition:scale bind:this={details} {...props}>
	<header>
		{item[4]}
	</header>
	<div>
		<details>
			<summary>Project Description</summary>
			<p>{@html item[21].replace(/(\\r)?\\n/g, '<br>')}</p>
		</details>
		<hr />
		<dl>
			<dt>Award Number</dt>
			<dd>{item[0] || '---'}</dd>
			<dt>Award Period</dt>
			<dd>{item[5] || '---'}</dd>

			<dt>Organization</dt>
			<dd>{item[6] || '---'}</dd>

			<dt>Primary Humanities Discipline</dt>
			<dd>{item[12] || '---'}</dd>

			<dt>Professional Body</dt>
			<dd>{item[13] || '---'}</dd>

			<dt>Grant Program Name</dt>
			<dd>{item[15] || '---'}</dd>

			<dt>Division or Office</dt>
			<dd>{item[16] || '---'}</dd>

			<dt>Awarded Outright</dt>
			<dd>
				{Number(item[19]) ? '$' + Number(item[19]).toLocaleString('en-US') : '---'}
			</dd>
		</dl>
		<hr />
		<p>
			Representative: <strong>{item[32]} {item[31]}</strong> ({item[30]}, {item[33]})<br />
			URL: <a href={item[34]}>{item[34]}</a><br />
			{item[35]}<br />
			Tel: {item[36]}
		</p>
		<p>
			{#if item[38]}
				Senator: <strong>{item[38]} {item[37]}</strong> ({item[39]})<br />
				URL: <a href={item[40]}>{item[40]}</a><br />
				{item[41]}<br />
				Tel: {item[42]}<br />
				Contact Form: <a href={item[43]}>{item[43]}</a><br />
				{#if item[45]}
					Twitter: <a href={`https://twitter.com/${item[45]}`}>@{item[45]}</a><br />
				{/if}
				{#if item[46]}
					Facebook: <a href={`https://www.facebook.com/${item[46]}`}>{item[46]}</a><br />
				{/if}
			{:else}
				No Senator Data
			{/if}
		</p>
		<p>
			{#if item[48]}
				Senator: <strong>{item[48]} {item[47]}</strong> ({item[49]})<br />
				URL: <a href={item[50]}>{item[50]}</a><br />
				{item[51]}<br />
				Tel: {item[52]}<br />
				Contact Form: <a href={item[53]}>{item[53]}</a><br />
				{#if item[54]}
					Twitter: <a href={`https://twitter.com/${item[54]}`}>@{item[54]}</a><br />
				{/if}
				{#if item[55]}
					Facebook: <a href={`https://www.facebook.com/${item[55]}`}>{item[55]}</a><br />
				{/if}
			{:else}
				No Senator Data
			{/if}
		</p>
	</div>
	<button onclick={() => close()}>Close</button>
</section>

<svelte:window
	onclick={(e) => e.composedPath().includes(details) || close()}
	onkeydown={({ key }) => key === 'Escape' && close()}
/>

<style>
	section {
		position: absolute;
		top: 5%;
		left: 50%;
		width: 90%;
		height: 90%;
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

	summary {
		font-weight: bold;
		color: var(--primary-color);
		font-size: 1.2rem;
	}

	details p {
		margin: 1rem 1rem;
	}

	div {
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		flex-grow: 1;
		overflow-y: auto;
	}

	dl {
		columns: 2;
	}

	dt,
	dd {
		break-inside: avoid;
	}

	dt {
		font-weight: bold;
		color: var(--primary-color);
		font-size: 1.1rem;
	}

	dd {
		padding-left: 0.5rem;
		margin-bottom: 0.5rem;
	}

	button {
		background-color: var(--primary-color);
		color: #fff;
		padding: 0.5rem 1rem;
		border: none;
		border-top: 1px solid var(--primary-color);
		cursor: pointer;

		&:hover {
			background-color: #fff;
			border-radius: 0 0 5px 5px;
			color: var(--primary-color);
		}
	}
</style>
