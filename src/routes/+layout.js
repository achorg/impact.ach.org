export const prerender = true;

/** @type {import('./$types').PageLoad} */
export async function load(/* { params } */) {
	const env = await import('$env/static/public');

	const commit = env.PUBLIC_COMMIT || 'development';
	const datetime = new Date().toISOString();

	return { commit, datetime };
}
