<script>
	import { tick } from 'svelte';
	import { computePosition, shift } from '@floating-ui/dom';
	import { findParentWithCSS } from '$lib';

	/**
	 * @typedef {Object} CheckboxMultiSelectProps
	 * @prop {Array<Object|Array<any>>} options
	 * @prop {string} selectId
	 * @prop {function} [onSelectedValuesUpdated]
	 * @prop {string} [placeHolder]
	 * @prop {string} [class]
	 */

	/** @type {CheckboxMultiSelectProps} */
	let {
		options,
		selectId,
		onSelectedValuesUpdated,
		placeHolder = 'Select an item...',
		...props
	} = $props();

	let filteredOptions = $state.raw([]);
	let selectedValues = $state.raw([]);
	let open = $state(false);
	let dropdown = $state();
	let input = $state();
	let selectEl = $state();
	let hasGroups = !Array.isArray(options);

	const resetFilteredOptions = () => {
		if (hasGroups) {
			filteredOptions = Object.values(options)
				.map((group) => group.options)
				.flat();
		} else {
			filteredOptions = options;
		}
	};

	const sortedOptions = $derived(
		// filteredOptions.toSorted(
		// 	(a, b) =>
		// 		selectedValues.includes(b.value) - selectedValues.includes(a.value) ||
		// 		a.label.localeCompare(b.label)
		// )
		filteredOptions.toSorted((a, b) => a.label.localeCompare(b.label))
	);

	const positionDropdown = () => {
		computePosition(input, dropdown, {
			placement: 'bottom-start',
			middleware: [shift({ padding: 2 })]
		}).then(({ x, y }) => {
			const inputTop = input.getBoundingClientRect().top;
			const bottom = findParentWithCSS(input, 'overflow', 'hidden')?.getBoundingClientRect().bottom;
			Object.assign(dropdown.style, {
				left: `${x}px`,
				top: `${y + 6}px`,
				maxHeight: `calc(${bottom ? bottom + 'px' : '100vh'} - ${inputTop + y + 10}px)`
			});
		});
	};

	const activateDropdown = async () => {
		if (open) return;
		resetFilteredOptions();
		open = true;
		positionDropdown();
		await tick();
		input.innerHTML = '';
		input.focus();
	};

	const closeDropdown = () => {
		open = false;
		input.innerHTML = selectedValues.length ? selectedValues.join(' | ') : placeHolder;
		input.blur();
	};

	const toggleDropdown = () => (open ? closeDropdown() : activateDropdown());

	const search = async () => {
		open = true;
		resetFilteredOptions();

		if (!input.innerHTML) return;

		if (input.innerText) {
			const searchParts = input.innerText.toLowerCase().split(' ');

			filteredOptions = filteredOptions.filter((option) =>
				searchParts.every((searchPart) => option.label.toLowerCase().includes(searchPart))
			);
		}
	};

	const selectedValuesUpdated = async () => {
		input.focus();
		await tick();
		onSelectedValuesUpdated?.(selectedValues);
	};
</script>

<div id={selectId} bind:this={selectEl} {...props} class:container={true}>
	<span
		class="input"
		role="searchbox"
		tabindex="-1"
		spellcheck="false"
		contenteditable="true"
		placeholder="Type to filter..."
		class:show-indicator={selectedValues.length}
		bind:this={input}
		oninput={search}
		onfocus={activateDropdown}
		onmousedown={(event) => {
			event.preventDefault();
			toggleDropdown();
		}}>{@html placeHolder}</span
	>
	{#if selectedValues.length}
		<button
			onclick={() => {
				selectedValues = [];
				selectedValuesUpdated();
			}}>{selectedValues.length}</button
		>
	{/if}

	<div class="dropdown" class:open bind:this={dropdown}>
		{#if hasGroups}
			{#each Object.keys(options).filter((group) => options[group].options) as group}
				{@const subOptions = options[group].options}
				{@const optionValues = subOptions.map((o) => o.value)}
				<label class="group">
					<input
						type="checkbox"
						checked={optionValues.every((option) => selectedValues.includes(option))}
						indeterminate={optionValues.some((option) => selectedValues.includes(option)) &&
							!optionValues.every((option) => selectedValues.includes(option))}
						onchange={({ target }) => {
							if (target.checked) {
								// select all options for this group
								selectedValues = [...new Set([...selectedValues, ...optionValues])];
							} else {
								// unselect all options for this group
								selectedValues = selectedValues.filter((option) => !optionValues.includes(option));
							}
							selectedValuesUpdated();
						}}
					/>
					{group} [{options[group].count}]
				</label>
				{#each subOptions as option}
					{#if filteredOptions.includes(option)}
						<label class="suboption">
							<input
								type="checkbox"
								value={option.value}
								bind:group={selectedValues}
								onchange={selectedValuesUpdated}
							/>
							{option.label}
						</label>
					{/if}
				{/each}
			{/each}
		{:else}
			{#each sortedOptions as option}
				{#if filteredOptions.includes(option)}
					<label>
						<input
							type="checkbox"
							value={option.value}
							bind:group={selectedValues}
							onchange={selectedValuesUpdated}
						/>
						{option.label}
					</label>
				{/if}
			{/each}
		{/if}
		{#if !filteredOptions.length}
			<span>No matching options</span>
		{/if}
	</div>
</div>

<svelte:window
	onclick={({ target }) => {
		if (open && !(dropdown.contains(target) || input.contains(target))) {
			closeDropdown();
		}
	}}
	onkeydown={({ key }) => {
		if (open && key === 'Escape') closeDropdown();
	}}
/>

<style lang="postcss">
	.container {
		position: relative;

		&:focus-visible {
			outline: none;
		}

		&:after {
			border-left: 5px solid transparent;
			border-right: 5px solid transparent;
			border-top: 5px solid currentColor;
			content: '';
			height: 0;
			margin-top: -2px;
			pointer-events: none;
			position: absolute;
			right: 8px;
			top: 50%;
			width: 0;
		}
	}

	.dropdown {
		background-color: inherit;
		border: 1px solid currentColor;
		border-radius: 4px;
		display: none;
		flex-direction: column;
		max-height: 90vh;
		overflow-y: auto;
		padding: 0.5em 0.5em 1em;
		position: absolute;
		width: max-content;
		z-index: 9;

		min-width: calc(100% + 3px);
		max-width: calc(100vw - 4px);

		&.open {
			display: flex;
		}
	}

	span.input {
		border-radius: var(--border-radius);
		cursor: pointer;
		display: inline-block;
		height: 100%;
		overflow: hidden;
		padding: 5px 11px 5px 0;
		text-overflow: ellipsis;
		white-space: nowrap;
		width: 100%;
		vertical-align: middle;

		&:focus-visible {
			outline: none;
		}

		&[contenteditable='true']:empty:before {
			content: attr(placeholder);
			opacity: 0.5;
			pointer-events: none;
		}

		&.show-indicator {
			padding: 5px 0;
			width: calc(100% - 40px);
		}
	}

	button {
		background: none;
		background-color: var(--primary-color);
		border: none;
		border-radius: 8px;
		color: #ffffff;
		display: block;
		font-family: sans-serif;
		font-size: 0.9rem;
		line-height: 1.1rem;
		opacity: 0.8;
		padding: 0 6px;
		position: absolute;
		right: 22px;
		top: 50%;
		transform: translateY(-50%);

		&:hover::after {
			appearance: none;
			background-color: white;
			border: none;
			border-radius: 8px;
			box-shadow: none;
			color: var(--primary-color);
			content: '×';
			cursor: pointer;
			font-size: 1.5rem;
			font-weight: bold;
			left: 0;
			padding: 0 3px;
			position: absolute;
			top: 0;
		}
	}

	label {
		display: flex;
		gap: 0.5rem;
		align-items: stretch;
		line-height: 20px;

		&.group {
			font-size: 1.1em;
			font-weight: bold;
			margin: 1em 0 0.5em;
		}

		&.suboption {
			margin-left: 10px;
			padding-left: 3em;
			text-indent: -3em;
		}

		input {
			margin-top: 2px;
		}
	}
</style>
