<script>
	import { sleep } from '$lib';

	import CheckboxMultiSelect from '$components/CheckboxMultiSelect.svelte';
	import SearchInput from '$components/SearchInput.svelte';
	import { tooltip } from '$lib/actions/tooltip';
	import { tooltip as tooltipWhenTruncated } from '$lib/actions/tooltip-when-truncated';

	import loaderWebP from '../img/loading.webp';

	/**
	 * @typedef {Object} Field
	 * @prop {string} key
	 * @prop {string} label
	 * @prop {number|string} accessor - Accessor (object key or array index) for the field.
	 * @prop {boolean} [html]
	 * @prop {boolean} [sortable]
	 * @prop {boolean} [searchable]
	 * @prop {boolean} [filterable]
	 * @prop {(value: any) => string} [format]
	 */

	/**
	 * @typedef {{[key: string]: number | string}} Item
	 */

	/**
	 * @typedef {Object} TableProps
	 * @prop {Array<Object|Array<any>>} data
	 * @prop {Field[]} fields
	 * @prop {string|number} keyAccessor - Accessor (object key or array index) for the primary key.
	 * @prop {(items: Item[]) => any} [onFilteredItemsUpdated]
	 * @prop {(event: MouseEvent, item: Item) => any} [onRowClick]
	 * @prop {string} [id]
	 * @prop {string} [class]
	 */

	/** @type {TableProps} */
	let { data, fields, keyAccessor, onFilteredItemsUpdated, onRowClick, ...props } = $props();

	let loading = $state(true);
	let tbody = $state();
	let scrollbarOffset = $state(0);

	let filterRowOpen = $state(false);

	let filteredItems = $state(/** @type {Item[]} */ (data));
	let filteredAndPagedItems = $state(/** @type {Item[]} */ ([]));
	let currentPage = $state(1);
	let pageSize = $state(20);
	let activeFilters = $state(/** @type {{[key: string]: number[] | string[]}} */ ({}));
	let searchParts = $state(/** @type {string[]} */ ([]));
	let sortOrder = $state();
	let thead = $state();

	const paginate = () => {
		filteredAndPagedItems = filteredItems.slice(
			0 + (currentPage - 1) * pageSize,
			0 + (currentPage - 1) * pageSize + pageSize
		);
		loading = false;
	};

	/**
	 * @param {string|number} text
	 * @param {boolean} [stripAccents]
	 * @returns {string}
	 */
	const normalizeText = (text, stripAccents = false) => {
		if (typeof text !== 'string') text = String(text);
		text = text.toLowerCase().replace(/\s+/g, ' ').trim();
		if (stripAccents) text = text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
		return text;
	};

	/**
	 * @param {Field} field
	 * @returns {{value: string, label: string}[]}
	 */
	const getOptions = (field) => {
		const { accessor } = field;
		const options = Object.entries(
			data.reduce((acc, item) => {
				const value = item[accessor];
				acc[value] = (acc[value] || 0) + 1;
				return acc;
			}, {})
		).map(([value, count]) => ({ value, label: `${value} (${count})` }));

		return options;
	};

	/**
	 * @param {string} text
	 * @returns {void}
	 */
	const prepSearchParts = (text) => {
		searchParts = text
			? normalizeText(text.replace(/<br>|[&/\\#,+()$~%.'":*?<>{}]|nbsp;/g, ' '))
					.split(' ')
					.slice(0, 8)
			: [];
	};

	/**
	 * @param {string|number} text
	 * @returns {string}
	 */
	const markupMatches = (text) => {
		if (typeof text !== 'string') text = String(text);
		const matchExtents = /** @type {Array<[number, number]>} */ ([]);
		const mergedExtents = /** @type {Array<[number, number]>} */ ([]);
		let markedUp = text;
		const searchContent = normalizeText(text);

		searchParts.forEach((searchPart) => {
			let idx = -1;
			while ((idx = searchContent.indexOf(searchPart, idx + 1)) > -1)
				matchExtents.push([idx, idx + searchPart.length]);
		});

		matchExtents
			.sort((a, b) => a[0] - b[0])
			.forEach(([start, end]) => {
				const previousExtent = mergedExtents[mergedExtents.length - 1];
				if (previousExtent && previousExtent[1] >= start) {
					previousExtent[1] = Math.max(previousExtent[1], end);
				} else {
					mergedExtents.push([start, end]);
				}
			});

		mergedExtents
			.sort((a, b) => b[0] - a[0])
			.forEach(([start, end]) => {
				markedUp = `${markedUp.substring(0, start)}<mark>${markedUp.substring(
					start,
					end
				)}</mark>${markedUp.substring(end)}`;
			});
		return markedUp;
	};

	const itemFilter = async () => {
		filteredItems = /** @type {Item[]} */ (data);
		if (activeFilters) {
			Object.entries(activeFilters).forEach(([field, filterArray]) => {
				if (!filterArray.length) return;
				const accessor = fields.find((f) => f.key === field)?.accessor;
				filteredItems = filteredItems.filter((item) => filterArray.includes(item[accessor]));
			});
		}
		if (searchParts.length) {
			const searchFields = fields.filter((field) => field.searchable);
			filteredItems = filteredItems.filter((item) =>
				searchParts.every((searchPart) =>
					searchFields.some(({ accessor }) => normalizeText(item[accessor]).includes(searchPart))
				)
			);
		}
		currentPage = 1;
		paginate();
	};

	/** @param {Field} field */
	const sortItems = async (field) => {
		loading = true;
		await sleep(0);

		const { key, accessor } = field;
		sortOrder = sortOrder === `${key}-asc` ? `${key}-desc` : `${key}-asc`;
		const asc = sortOrder.endsWith('asc');
		filteredItems = filteredItems.sort((a, b) => {
			if (a[accessor] < b[accessor]) return asc ? -1 : 1;
			if (a[accessor] > b[accessor]) return asc ? 1 : -1;
			return 0;
		});
		currentPage = 1;
		paginate();
	};

	/** @param {string} searchValue */
	const search = async (searchValue) => {
		loading = true;
		await sleep(0);
		prepSearchParts(searchValue);
		itemFilter();
	};

	$effect(() => {
		const resizeObserver = new ResizeObserver(
			([{ target }]) =>
				(scrollbarOffset =
					/** @type {HTMLTableSectionElement} */ (target).offsetWidth - target.scrollWidth)
		);
		resizeObserver.observe(tbody);
	});

	$effect(() => paginate());
	$effect(() => onFilteredItemsUpdated?.(filteredItems));
</script>

<div class="controls">
	{#if fields.some(({ searchable }) => searchable)}
		<SearchInput
			oninput={(/** @type {InputEvent} */ event) =>
				search(/** @type {HTMLInputElement} */ (event.target).value)}
		/>
	{/if}
	{#if fields.some(({ filterable }) => filterable)}
		<button
			class="show-filters"
			aria-label="Show/Hide Filters"
			onclick={() => (filterRowOpen = !filterRowOpen)}
			class:open={filterRowOpen}
			use:tooltip={{ content: filterRowOpen ? 'Hide Filters' : 'Show Filters' }}
		>
			{#if filterRowOpen}
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<path
						d="M8 4h12v2.172a2 2 0 0 1 -.586 1.414l-3.914 3.914m-.5 3.5v4l-6 2v-8.5l-4.48 -4.928a2 2 0 0 1 -.52 -1.345v-2.227"
					/>
					<path d="M3 3l18 18" />
				</svg>
			{:else}
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<path
						d="M4 4h16v2.172a2 2 0 0 1 -.586 1.414l-4.414 4.414v7l-6 2v-8.5l-4.48 -4.928a2 2 0 0 1 -.52 -1.345v-2.227z"
					/>
				</svg>
			{/if}
		</button>
	{/if}
</div>

<table
	aria-label="Jewish Cookbook Recipes"
	aria-rowcount={pageSize}
	style={`
	  --n-columns: ${fields.length};
		--scrollbar-offset: ${scrollbarOffset}px;
		--loader: url(${loaderWebP});
	`}
	{...props}
>
	<thead bind:this={thead}>
		<tr>
			{#each fields as field}
				{#if field.sortable}
					<th
						scope="col"
						aria-sort={(sortOrder === `${field.key}-asc` && 'ascending') ||
							(sortOrder === `${field.key}-desc` && 'descending') ||
							null}
					>
						<button onclick={() => sortItems(field)}>
							{field.label}
						</button>
					</th>
				{:else if field.label}
					<th scope="col">{field.label}</th>
				{:else}
					<td></td>
				{/if}
			{/each}
		</tr>
		<tr class="filters" class:open={filterRowOpen}>
			{#each fields as field}
				<td>
					{#if field.filterable}
						<CheckboxMultiSelect
							class="checkbox-multiselect"
							options={getOptions(field)}
							selectId="abc"
							onSelectedValuesUpdated={async (/** @type {string[]} */ values) => {
								activeFilters[field.key] = values;
								loading = true;
								await sleep(0);
								itemFilter();
							}}
						/>
					{/if}
				</td>
			{/each}
		</tr>
	</thead>

	<tbody
		bind:this={tbody}
		class:loading
		onscroll={(event) => {
			thead.style.translate = `-${/** @type {HTMLElement} */ (event.target)?.scrollLeft}px 0`;
		}}
	>
		{#each filteredAndPagedItems as item (item[keyAccessor])}
			<tr onclick={(event) => onRowClick?.(event, item)}>
				{#each fields as field, i}
					{@const formattedValue = field.format
						? field.format(item[field.accessor])
						: item[field.accessor]}
					{@const value =
						searchParts && field.searchable ? markupMatches(formattedValue) : formattedValue}
					{#if i === 0}
						<th scope="row" use:tooltipWhenTruncated={{ content: value }}>{@html value}</th>
					{:else}
						<td use:tooltipWhenTruncated={{ content: value }}>{@html value}</td>
					{/if}
				{/each}
			</tr>
		{/each}
	</tbody>
</table>
<div class="pagination">
	{#if filteredItems.length === 0}
		No results
	{:else}
		{@const pageStart = pageSize * (currentPage - 1) + 1}
		<span aria-live="assertive">
			Showing <strong>{pageStart}</strong>&nbsp;to&nbsp;<strong>
				{Math.min(pageStart + pageSize - 1, filteredItems.length)}
			</strong>&nbsp;of&nbsp;<strong>{filteredItems.length.toLocaleString()}</strong>
		</span>

		<button disabled={currentPage === 1} onclick={() => (currentPage -= 1)}>
			&laquo; Previous
		</button>
		<button
			disabled={currentPage * pageSize >= filteredItems.length}
			onclick={() => (currentPage += 1)}
		>
			Next &raquo;
		</button>
	{/if}
</div>

<style>
	.controls {
		display: flex;
		gap: 1rem;
		justify-content: flex-start;
		padding-left: 2px;
		margin-bottom: 0.5rem;
	}

	table {
		--n-columns: 2;
		--row-height: 35px;
		--scrollbar-offset: 0px;

		display: contents;
		border-collapse: collapse;
	}

	thead,
	tbody {
		display: grid;
		min-width: 100%;
		grid-template-columns: repeat(var(--n-columns), 1fr);
		flex: 0 1 auto;
	}

	thead {
		padding-right: var(--scrollbar-offset);
		z-index: 1;
	}

	tr.filters {
		--transition-duration: 0.5s;
		td {
			height: 0px;
			transition: height var(--transition-duration) ease-in-out;
		}

		&.open td {
			height: 40px;
			/* overflow: visible; */
			animation-duration: 0;
			animation-delay: var(--transition-duration);
			animation-name: set-overflow;
			animation-fill-mode: forwards;
		}
	}

	tbody {
		overflow-y: auto;
		position: relative;

		&.loading::after {
			background: rgba(255, 255, 255, 0.8) var(--loader) no-repeat center;
			content: '';
			display: grid;
			height: 100%;
			place-items: center;
			position: absolute;
			width: 100%;
		}
	}

	tr {
		display: contents;
	}

	th,
	td {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	thead th {
		padding-right: 1rem;
		position: relative;
		text-align: left;
		font-weight: normal;

		button {
			appearance: none;
			background-color: transparent;
			border: none;
			color: inherit;
			cursor: pointer;
			font: inherit;
			height: 100%;
			left: 0;
			overflow: hidden;
			padding: inherit;
			position: absolute;
			text-align: inherit;
			text-overflow: ellipsis;
			top: 0;
			white-space: nowrap;
			width: 100%;

			&:before,
			&:after {
				border: 6px solid transparent;
				position: absolute;
				display: block;
				content: '';
				height: 0;
				right: 0.5rem;
				top: 50%;
				width: 0;
			}
		}

		&:not([aria-sort]) button:before,
		&[aria-sort='ascending'] button:before {
			border-bottom-color: currentColor;
			margin-top: -14px;
		}

		&:not([aria-sort]) button:after,
		&[aria-sort='descending'] button:after {
			border-top-color: currentColor;
			margin-top: 3px;
		}
	}

	tbody th {
		text-align: left;
	}

	td,
	th {
		padding: 0 0.5rem;
		height: var(--row-height);
		line-height: var(--row-height);
	}

	.pagination {
		align-items: center;
		display: flex;
		gap: 1rem;
		margin-top: 2rem;
		padding: 0 0.5rem;

		span {
			flex-grow: 1;
		}
	}

	button.show-filters {
		background-color: var(--primary-color);
		border: 1px solid #d2d6dc;
		border-radius: 5px;
		color: #ffffff;
		cursor: pointer;
		line-height: 1;
		padding: 5px 14px;
		transition: all 0.2s ease-in-out;
		user-select: none;
		white-space: nowrap;

		&:not([disabled]):hover,
		&:focus-visible,
		&.open {
			background-color: #f7f7f7;
			border: 1px solid var(--primary-color);
			color: var(--primary-color);
		}

		&.open:hover {
			background-color: var(--primary-color);
			border: 1px solid #d2d6dc;
			color: #ffffff;
		}

		&:focus-visible {
			outline: 2px solid var(--primary-color);
			outline-offset: 2px;
		}

		svg {
			pointer-events: none;
		}
	}

	@keyframes set-overflow {
		from {
			overflow: hidden;
		}

		to {
			overflow: initial;
		}
	}
</style>
