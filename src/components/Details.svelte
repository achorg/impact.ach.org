<script>
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

<section bind:this={details} {...props}>
	<header>
		{item[4]}
	</header>
	<div>
		<details>
			<summary>Project Description</summary>
			{@html item[21].replace(/(\\r)?\\n/g, '<br>')}
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
			Representative: {item[32]}
			{item[31]} ({item[30]}, {item[33]})<br />
			URL: <a href={item[34]}>{item[34]}</a><br />
			{item[35]}<br />
			Tel: {item[36]}
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
	}

	header {
		font-weight: bold;
		font-size: 1.4rem;
		background-color: var(--primary-color);
		color: #fff;
		padding: 0.5rem;
	}

	summary {
		font-weight: bold;
		color: var(--primary-color);
		font-size: 1.2rem;
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

	dt {
		font-weight: bold;
		color: var(--primary-color);
		font-size: 1.2rem;
	}

	dd {
		padding-left: 0.5rem;
		margin-bottom: 0.5rem;
	}
</style>
