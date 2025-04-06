<script>
	import Table from '$components/Table.svelte';
	/** @import { Item } from '$components/Table.svelte' */

	import awards from '../data/terminated-awards.2025-04-04.json';

	let filteredListItems = $state(/** @type {Item[]} */ ([]));
	let filteredItemsCount = $derived(filteredListItems?.length);
	let filteredItemsValue = $derived(
		filteredListItems.reduce((acc, item) => acc + Number(item[19]), 0)
	);

	/** @param {string} text */
	const titleCase = (text) => {
		return text
			.toLowerCase()
			.split(' ')
			.map((word) => word.charAt(0).toUpperCase() + word.substring(1))
			.join(' ');
	};

	/** @param {string} url */
	const formatLink = (url) => {
		if (!url) return '';
		return `
		  <a href="${url}" aria-label="View on SearchWorks">
				${externalLinkSvg}
			</a>`;
	};

	const externalLinkSvg = `
		<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
			<path d="M12 6h-6a2 2 0 0 0 -2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-6" />
			<path d="M11 13l9 -9" />
			<path d="M15 4h5v5" />
		</svg>	
	`;

	const fields = [
		{
			key: 'project-title',
			label: 'Project Title',
			accessor: 4,
			sortable: true,
			// format: titleCase,
			searchable: true
		},
		{
			key: 'organization',
			label: 'Organization',
			accessor: 6,
			sortable: true,
			searchable: true,
			filterable: true
		},
		{ key: 'state', label: 'State', accessor: 8, sortable: true, filterable: true },
		{
			key: 'discipline',
			label: 'Discipline',
			accessor: 14,
			sortable: true,
			searchable: true,
			filterable: true
		},
		{
			key: 'grant-program',
			label: 'Grant Program',
			accessor: 15,
			sortable: true,
			searchable: true,
			filterable: true
		},
		{
			key: 'division-or-office',
			label: 'Div./Office',
			accessor: 16,
			sortable: true,
			searchable: true,
			filterable: true
		},
		{
			key: 'congressional-district',
			label: 'District',
			accessor: 30,
			sortable: true,
			searchable: true,
			filterable: true
		}
	];

	const onFilteredItemsUpdated = (/** @type {Item[]} */ items) => {
		filteredListItems = items;
	};
</script>

<div class="totals">
	Terminated Awards Filtered: <span>{filteredItemsCount.toLocaleString()}</span>; Total Value:
	<span>${filteredItemsValue.toLocaleString()}</span>
</div>
<Table data={awards} {fields} keyAccessor={0} id="awards-table" {onFilteredItemsUpdated} />

<style>
	.totals span {
		font-weight: bold;
		color: var(--primary-color);
		font-size: 1.2rem;
	}

	:global(#awards-table) {
		:global {
			thead,
			tbody {
				grid-template-columns:
					minmax(250px, 1.5fr) /* Project Title */
					minmax(150px, 1fr) /* Organization */
					80px /* State */
					minmax(115px, 0.5fr) /* Discipline */
					minmax(115px, 0.5fr) /* Grant Program */
					minmax(115px, 0.5fr) /* Division or Office */
					100px /* Congressional District */;
			}

			thead {
				border-bottom: 2px solid currentColor;

				th {
					font-size: 1.2rem;
					font-weight: bold;
					height: 55px;
					line-height: 55px;
				}
			}

			tbody {
				/* min-height: calc(var(--row-height) * 2); */

				tr:nth-child(even) td,
				tr:nth-child(even) th {
					background: var(--tertiary-color);
				}

				tr:hover td,
				tr:hover th {
					background: var(--secondary-color);
				}
			}

			td:nth-child(3) {
				text-align: center;
			}

			td:nth-child(7) {
				text-align: center;
			}

			thead th button::before,
			thead th button::after {
				opacity: 0.3;
			}

			thead th[aria-sort] button::before,
			thead th[aria-sort] button::after {
				opacity: 1;
			}

			thead th button:hover {
				background-color: var(--secondary-color);

				&::before,
				&::after {
					opacity: 1;
				}
			}

			/* 960px is where the table starts to overflow horizontally */
			@media screen and (max-width: 959px) {
				td.search {
					justify-content: flex-start;
					margin-top: 1rem;
				}
			}
		}
	}

	:global(.pagination) {
		flex-wrap: wrap;
		:global {
			button {
				background-color: var(--primary-color);
				border: 1px solid #d2d6dc;
				border-radius: 5px;
				color: #ffffff;
				cursor: pointer;
				line-height: 1;
				padding: 5px 14px;
				user-select: none;
				white-space: nowrap;

				&[disabled] {
					cursor: not-allowed;
					opacity: 0.5;
				}

				&:not([disabled]):hover,
				&:focus-visible {
					background-color: #f7f7f7;
					color: #3c4257;
				}

				&:focus-visible {
					outline: 2px solid var(--primary-color);
					outline-offset: 2px;
				}
			}
		}
	}
</style>
