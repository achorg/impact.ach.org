<script>
	import Popup from './Popup.svelte';
	/** @import { Item } from '$components/Table.svelte' */

	import accessors from '../data/accessors.json';

	const {
		awardNumber,
		projectTitle,
		awardPeriod,
		organization,
		primaryHumanitiesDiscipline,
		professionalBody,
		grantProgram,
		divisionOrOffice,
		awardedOutright,
		description,

		district,
		repFirstName,
		repLastName,
		repParty,
		repUrl,
		repAddress,
		repPhone,
		sen1FirstName,
		sen1LastName,
		sen1Party,
		sen1Url,
		sen1Address,
		sen1Phone,
		sen1ContactForm,
		sen1Twitter,
		sen1Facebook,
		sen2FirstName,
		sen2LastName,
		sen2Party,
		sen2Url,
		sen2Address,
		sen2Phone,
		sen2ContactForm,
		sen2Twitter,
		sen2Facebook
	} = accessors;

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
		Representative: <strong>{item[repLastName]} {item[repFirstName]}</strong> ({item[district]}, {item[
			repParty
		]})<br />
		URL: <a href={item[repUrl]}>{item[repUrl]}</a><br />
		{item[repAddress]}<br />
		Tel: {item[repPhone]}
	</p>
	<p>
		{#if item[sen1LastName]}
			Senator: <strong>{item[sen1FirstName]} {item[sen1LastName]}</strong> ({item[sen1Party]})<br />
			URL: <a href={item[sen1Url]}>{item[sen1Url]}</a><br />
			{item[sen1Address]}<br />
			Tel: {item[sen1Phone]}<br />
			Contact Form: <a href={item[sen1ContactForm]}>{item[sen1ContactForm]}</a><br />
			{#if item[sen1Twitter]}
				Twitter: <a href={`https://twitter.com/${item[sen1Twitter]}`}>@{item[sen1Twitter]}</a><br />
			{/if}
			{#if item[sen1Facebook]}
				Facebook: <a href={`https://www.facebook.com/${item[sen1Facebook]}`}>{item[sen1Facebook]}</a
				><br />
			{/if}
		{:else}
			No Senator Data
		{/if}
	</p>
	<p>
		{#if item[sen2LastName]}
			Senator: <strong>{item[sen2FirstName]} {item[sen2LastName]}</strong> ({item[sen2Party]})<br />
			URL: <a href={item[sen2Url]}>{item[sen2Url]}</a><br />
			{item[sen2Address]}<br />
			Tel: {item[sen2Phone]}<br />
			Contact Form: <a href={item[sen2ContactForm]}>{item[sen2ContactForm]}</a><br />
			{#if item[sen2Twitter]}
				Twitter: <a href={`https://twitter.com/${item[sen2Twitter]}`}>@{item[sen2Twitter]}</a><br />
			{/if}
			{#if item[sen2Facebook]}
				Facebook: <a href={`https://www.facebook.com/${item[sen2Facebook]}`}>{item[sen2Facebook]}</a
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
		font-weight: bold;
		color: var(--primary-color);
		font-size: 1.2rem;
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
		font-weight: bold;
		color: var(--primary-color);
		font-size: 1.1rem;
	}

	dd {
		padding-left: 0.5rem;
		margin-bottom: 0.5rem;
	}
</style>
