<script>
	import { mount, unmount } from 'svelte';

	import Details from '$components/Details.svelte';
	import Table from '$components/Table.svelte';
	/** @import { Item } from '$components/Table.svelte' */
	import { tooltip } from '$lib/actions/tooltip';

	import awards from '../data/terminated-awards.2025-04-04.json';
	import accessors from '../data/accessors.json';

	let filteredListItems = $state(/** @type {Item[]} */ ([]));
	let filteredItemsCount = $derived(filteredListItems?.length);
	let filteredItemsValue = $derived(
		filteredListItems.reduce((acc, item) => acc + Number(item[accessors.awardedOutright]), 0)
	);

	let proportionOfFederalBudget = $derived.by(() => {
		const prop = filteredItemsValue / (6.752 * 1000000000000);
		switch (true) {
			case prop < 0.00000001:
				return 'less than one millionth of 1';
			case prop < 0.0000001:
				return 'less than one hundred-thousandth of 1';
			case prop < 0.000001:
				return 'less than one ten-thousandth of 1';
			case prop < 0.00001:
				return 'less than one thousandth of 1';
			default:
				return prop.toPrecision(2);
		}
	});

	const fields = [
		{
			key: 'project-title',
			label: 'Project Title',
			accessor: accessors.projectTitle,
			sortable: true,
			searchable: true
		},
		{
			key: 'state',
			label: 'State',
			accessor: accessors.orgState,
			sortable: true,
			filterable: true
		},
		{
			key: 'discipline',
			label: 'Discipline',
			accessor: accessors.discipline,
			sortable: true,
			searchable: true,
			filterable: true
		},
		{
			key: 'grant-program',
			label: 'Grant Program',
			accessor: accessors.grantProgram,
			sortable: true,
			searchable: true,
			filterable: true
		},
		{
			key: 'division-or-office',
			label: 'Div./Office',
			accessor: accessors.divisionOrOffice,
			sortable: true,
			searchable: true,
			filterable: true
		},
		{
			key: 'congressional-district',
			label: 'District',
			accessor: accessors.district,
			sortable: true,
			filterable: true
		}
	];

	const onFilteredItemsUpdated = (/** @type {Item[]} */ items) => {
		filteredListItems = items;
	};

	const onRowClick = async (event, /** @type {Item} */ item) => {
		event.stopPropagation();
		const details = mount(Details, {
			target: document.body,
			props: { item, close: () => unmount(details) }
		});
	};
</script>

<div class="totals">
	Terminated&nbsp;Awards&nbsp;Filtered:&nbsp;<span>{filteredItemsCount.toLocaleString()}</span>;
	Total&nbsp;Value:&nbsp;<span>${filteredItemsValue.toLocaleString()}</span>
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
		use:tooltip={{ content: `${proportionOfFederalBudget}% of the Federal Budget` }}
	>
		<path d="M12 3c7.2 0 9 1.8 9 9s-1.8 9 -9 9s-9 -1.8 -9 -9s1.8 -9 9 -9z" />
		<path d="M12 16v.01" />
		<path d="M12 13a2 2 0 0 0 .914 -3.782a1.98 1.98 0 0 0 -2.414 .483" />
	</svg>
</div>
<Table
	data={awards}
	{fields}
	keyAccessor={0}
	id="awards-table"
	{onFilteredItemsUpdated}
	{onRowClick}
/>

<style>
	.totals {
		margin-bottom: 1rem;
		span {
			font-weight: bold;
			color: var(--primary-color);
			font-size: 1.2rem;
		}

		svg {
			display: inline-block;
			margin-left: 0.25rem;
			vertical-align: text-bottom;
		}
	}

	:global(#awards-table) {
		:global {
			thead,
			tbody {
				grid-template-columns:
					minmax(250px, 1.3fr) /* Project Title */
					/* minmax(150px, 1fr) /* Organization */
					80px /* State */
					minmax(115px, 0.35fr) /* Discipline */
					minmax(115px, 0.5fr) /* Grant Program */
					minmax(115px, 0.35fr) /* Division or Office */
					100px /* Congressional District */;
			}

			thead {
				th {
					font-size: 1.2rem;
					font-weight: bold;
					height: 55px;
					line-height: 55px;
				}
			}

			tbody {
				/* min-height: calc(var(--row-height) * 2); */
				border-top: 2px solid currentColor;

				th {
					font-weight: 600;
				}

				tr:nth-child(even) td,
				tr:nth-child(even) th {
					background: var(--tertiary-color);
				}

				tr:hover td,
				tr:hover th {
					background: var(--secondary-color);
				}
			}

			td:nth-child(2) {
				text-align: center;
			}

			td:nth-child(6) {
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

			@media screen and (max-width: 959px) {
				/* td.search {
					justify-content: flex-start;
					margin-top: 1rem;
				} */
			}
		}
	}

	:global(.pagination) {
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
