<script>
	import Popup from './Popup.svelte';
	/** @import { Item } from '$components/Table.svelte' */

	import accessors from '../data/accessors.json';
	import representativesByDistrict from '../data/representatives.2025-04-23.json';

	const {
		awardNumber,
		discipline,
		primaryHumanitiesDiscipline,
		projectTitle,
		awardPeriod,
		professionalBody,
		organization,
		orgState,
		divisionOrOffice,
		grantProgram,
		awardedOutright,
		description,
		district
	} = Object.fromEntries(accessors.awards.map((key, i) => [key, i]));

	const {
		repLastName,
		repFirstName,
		repParty,
		repUrl,
		repAddress,
		repPhone,
		sen1LastName,
		sen1FirstName,
		sen1Party,
		sen1Url,
		sen1Address,
		sen1Phone,
		sen1ContactForm,
		sen1Twitter,
		sen1Facebook,
		sen2LastName,
		sen2FirstName,
		sen2Party,
		sen2Url,
		sen2Address,
		sen2Phone,
		sen2ContactForm,
		sen2Twitter,
		sen2Facebook
	} = Object.fromEntries(accessors.representatives.map((key, i) => [key, i]));

	const reps = representativesByDistrict[item[district]] || [];

	/**
	 * @typedef {Object} DetailsProps
	 * @prop {Item} item
	 * @prop {function} close
	 */

	/** @type {DetailsProps} */
	let { item, close } = $props();
</script>

{#snippet header()}
	{item[projectTitle]}
{/snippet}

{#snippet content()}
	<details>
		<summary>Project Description</summary>
		<p>{@html item[description].replace(/(\\r)?\\n/g, '<br>')}</p>
	</details>
	<hr />
	<dl>
		<dt>Award Number</dt>
		<dd>{item[awardNumber] || '---'}</dd>
		<dt>Award Period</dt>
		<dd>{item[awardPeriod] || '---'}</dd>

		<dt>Organization</dt>
		<dd>{item[organization] || '---'}</dd>

		<dt>Primary Humanities Discipline</dt>
		<dd>{item[primaryHumanitiesDiscipline] || '---'}</dd>

		<dt>Professional Body</dt>
		<dd>{item[professionalBody] || '---'}</dd>

		<dt>Grant Program Name</dt>
		<dd>{item[grantProgram] || '---'}</dd>

		<dt>Division or Office</dt>
		<dd>{item[divisionOrOffice] || '---'}</dd>

		<dt>Awarded Outright</dt>
		<dd>
			{Number(item[awardedOutright])
				? '$' + Number(item[awardedOutright]).toLocaleString('en-US')
				: '---'}
		</dd>
	</dl>
	<hr />
	<p>
		{#if reps[repLastName]}
			Representative: <strong>{reps[repLastName]} {reps[repFirstName]}</strong> ({item[district]}, {reps[
				repParty
			]})<br />
			URL: <a href={reps[repUrl]}>{reps[repUrl]}</a><br />
			{reps[repAddress]}<br />
			Tel: {reps[repPhone]}
		{:else}
			No Representative Data
		{/if}
	</p>
	<p>
		{#if reps[sen1LastName]}
			Senator: <strong>{reps[sen1FirstName]} {reps[sen1LastName]}</strong> ({reps[sen1Party]})<br />
			URL: <a href={reps[sen1Url]}>{reps[sen1Url]}</a><br />
			{reps[sen1Address]}<br />
			Tel: {reps[sen1Phone]}<br />
			Contact Form: <a href={reps[sen1ContactForm]}>{reps[sen1ContactForm]}</a><br />
			{#if reps[sen1Twitter]}
				Twitter: <a href={`https://twitter.com/${reps[sen1Twitter]}`}>@{reps[sen1Twitter]}</a><br />
			{/if}
			{#if reps[sen1Facebook]}
				Facebook: <a href={`https://www.facebook.com/${reps[sen1Facebook]}`}>{reps[sen1Facebook]}</a
				><br />
			{/if}
		{:else}
			No Senator Data
		{/if}
	</p>
	<p>
		{#if reps[sen2LastName]}
			Senator: <strong>{reps[sen2FirstName]} {reps[sen2LastName]}</strong> ({reps[sen2Party]})<br />
			URL: <a href={reps[sen2Url]}>{reps[sen2Url]}</a><br />
			{reps[sen2Address]}<br />
			Tel: {reps[sen2Phone]}<br />
			Contact Form: <a href={reps[sen2ContactForm]}>{reps[sen2ContactForm]}</a><br />
			{#if reps[sen2Twitter]}
				Twitter: <a href={`https://twitter.com/${reps[sen2Twitter]}`}>@{reps[sen2Twitter]}</a><br />
			{/if}
			{#if reps[sen2Facebook]}
				Facebook: <a href={`https://www.facebook.com/${reps[sen2Facebook]}`}>{reps[sen2Facebook]}</a
				><br />
			{/if}
		{:else}
			No Senator Data
		{/if}
	</p>
{/snippet}

<Popup {header} {content} {close} />

<style>
	summary {
		color: var(--primary-color);
		font-size: 1.2rem;
		font-weight: bold;
	}

	details p {
		margin: 1rem 1rem;
	}

	dl {
		columns: 2;
	}

	dt,
	dd {
		break-inside: avoid;
	}

	dt {
		color: var(--primary-color);
		font-size: 1.1rem;
		font-weight: bold;
	}

	dd {
		break-before: avoid;
		margin-bottom: 0.5rem;
		padding-left: 0.5rem;
	}
</style>
