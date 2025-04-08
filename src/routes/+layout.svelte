<script>
	import { base } from '$app/paths';
	import '@fontsource-variable/libre-franklin';
	import '../styles/reset.css';
	import '../styles/base.css';

	import achLogo from '../img/logo.png';

	import { mount, unmount } from 'svelte';
	import About from '$components/About.svelte';
	import { tooltip } from '$lib/actions/tooltip';

	import { onMount } from 'svelte';

	onMount(() => {
		if (localStorage.getItem('about-shown')) return;

		const about = mount(About, {
			target: document.body,
			props: { close: () => unmount(about) }
		});

		localStorage.setItem('about-shown', 'true');
	});
</script>

<svelte:head>
	<title>NEH Grants 2025</title>
	<meta name="description" content="NEH Grants 2025" />
</svelte:head>

<header>
	<h1>
		<a href="{base}/">NEH Grants 2025</a>
		<button
			aria-label="About this data"
			onclick={(/** @type {MouseEvent} */ event) => {
				event.stopPropagation();
				const about = mount(About, {
					target: document.body,
					props: { close: () => unmount(about) }
				});
			}}
			use:tooltip={{ content: 'About this data' }}
		>
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
				<path d="M12 9h.01" /><path d="M11 12h1v4h1" />
				<path d="M12 3c7.2 0 9 1.8 9 9s-1.8 9 -9 9s-9 -1.8 -9 -9s1.8 -9 9 -9z" /></svg
			>
		</button>
	</h1>
	<a href="https://ach.org/" target="_blank" rel="noopener noreferrer">
		<img src={achLogo} height="40" alt="Association for Computing and the Humanities" />
	</a>
</header>

<main>
	<slot />
</main>

<style>
	header {
		align-items: center;
		display: flex;
		flex-wrap: wrap-reverse;
		justify-content: space-between;

		h1 a {
			text-decoration: none;

			&:hover {
				border-bottom: 1px solid currentColor;
			}
		}

		img {
			filter: invert(27%) sepia(17%) saturate(873%) hue-rotate(171deg) brightness(91%) contrast(88%);
		}

		button {
			appearance: none;
			background-color: transparent;
			border: none;
			color: inherit;
			cursor: pointer;
			font: inherit;
			overflow: hidden;
			padding: inherit;
			text-align: inherit;
		}
	}

	main {
		overflow: hidden;
		flex: 1 1 auto;
		display: flex;
		flex-direction: column;
	}
</style>
