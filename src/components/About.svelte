<script>
	import Popup from './Popup.svelte';

	/**
	 * @typedef {Object} AboutProps
	 * @prop {function} close
	 */

	/** @type {AboutProps} */
	let { close } = $props();
</script>

{#snippet content()}
	<p>
		This database includes National Endowment for the Humanities (NEH) grants that were canceled by
		DOGE as of Tuesday, April 8th. We understand that around 40 projects remain funded, including
		some that have been reinstated. Please reach out if a cancelled grant has not been included by
		emailing comms@ach.org, or if you see a grant on this list that has been reinstated.
	</p>

	<p>
		“Discipline” is challenging for many of these grants, and was extrapolated from the disciplinary
		tagging system used in the NEH database, mapping to the discipline of major professional
		associations in the US.
	</p>

	<p>
		The funding numbers are the amount awarded by NEH and represent a maximum cap of money lost by
		the project. Most had spent down some of their funds, but lost whatever remained to finish the
		project.
	</p>

	<p>
		For now, the <a href="https://apps.neh.gov/publicquery/Default.aspx" target="_blank"
			>NEH Award Search database</a
		> is still available to look up individual grants by title.
	</p>
{/snippet}

<Popup {content} {close} />

<style>
	p {
		font-size: 1.4rem;
		padding: 0.5rem min(1rem, 1vw);

		&:first-child {
			margin-top: 1.5rem;
		}

		&:last-child {
			margin-bottom: 2rem;
		}
	}
</style>
