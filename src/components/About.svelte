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
		This database includes National Endowment for the Humanities (NEH) grants that we understand
		were canceled by DOGE as of Thursday, April 3rd. It does not include individual fellowships at
		this point. Our understanding is that this is the majority of currently-funded NEH grants, and
		some projects do not appear in this database. Please reach out if a cancelled grant has not been
		included by emailing comms@ach.org.
	</p>

	<p>
		“Discipline” is challenging for many of these grants, and was extrapolated from the disciplinary
		tagging system used in the NEH database, mapping to the discipline of major professional
		associations in the US.
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
		padding: 0.5rem 1rem;

		&:first-child {
			margin-top: 1.5rem;
		}

		&:last-child {
			margin-bottom: 2rem;
		}
	}
</style>
