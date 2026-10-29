// GitHub and Make Core lookups for linked refs. Ported from wp-source-of-truth's check-status.mjs,
// minus its direct Trac requests (Trac blocks them).

import { execFileSync } from 'node:child_process';

let ghCli = null;
const hasGh = () => {
	if ( ghCli === null ) {
		try {
			execFileSync( 'gh', [ 'auth', 'status' ], { stdio: 'ignore' } );
			ghCli = true;
		} catch {
			ghCli = false;
		}
	}
	return ghCli;
};

// `gh api` when gh is signed in, otherwise fetch with GITHUB_TOKEN, otherwise anonymous.
export async function ghApi( path ) {
	if ( hasGh() ) return JSON.parse( execFileSync( 'gh', [ 'api', path ], { encoding: 'utf8', maxBuffer: 1 << 24 } ) );
	const headers = { Accept: 'application/vnd.github+json', 'User-Agent': 'wp-sot-scan' };
	if ( process.env.GITHUB_TOKEN ) headers.Authorization = `Bearer ${ process.env.GITHUB_TOKEN }`;
	const res = await fetch( `https://api.github.com/${ path }`, { headers } );
	if ( ! res.ok ) throw new Error( `${ res.status } ${ path }` );
	return res.json();
}

const sleep = ( ms ) => new Promise( ( r ) => setTimeout( r, ms ) );
let lastSearch = 0;

// The search API allows 30 requests a minute.
async function ghSearch( path ) {
	const wait = lastSearch + 2100 - Date.now();
	lastSearch = Date.now() + Math.max( wait, 0 );
	if ( wait > 0 ) await sleep( wait );
	try {
		return await ghApi( path );
	} catch {
		// Secondary rate limit: wait a minute and try once more.
		await sleep( 61000 );
		return ghApi( path );
	}
}

export async function lookupGithub( ref, gh = ghApi ) {
	try {
		const it = await gh( `repos/${ ref.repo }/issues/${ ref.number }` );
		const snap = { title: it.title, state: it.pull_request?.merged_at ? 'merged' : it.state };
		if ( it.milestone?.title ) snap.milestone = it.milestone.title;
		return snap;
	} catch ( e ) {
		return { title: '', state: 'unknown', error: String( e.message || e ) };
	}
}

export async function lookupDevnote( ref, fetchFn = fetch ) {
	try {
		const res = await fetchFn( ref.url, { headers: { 'User-Agent': 'wp-sot-scan' } } );
		if ( res.status === 404 || res.status === 410 ) return { title: '', state: 'missing' };
		if ( ! res.ok ) return { title: '', state: 'unknown', error: `${ res.status }` };
		const raw = ( await res.text() ).match( /<title>([^<]*)<\/title>/ )?.[ 1 ] ?? '';
		const title = raw.replace( /&#8211;|&ndash;/g, '–' ).replace( /\s+–\s+Make WordPress Core\s*$/, '' ).replace( /&amp;/g, '&' ).trim();
		return { title, state: 'ok' };
	} catch ( e ) {
		return { title: '', state: 'unknown', error: String( e.message || e ) };
	}
}

// Core commits are mirrored to WordPress/wordpress-develop with "Fixes #N" / "See #N" in the
// message, and patches live there as PRs, so GitHub stands in for Trac.
export async function tracViaGithub( number, gh = ghSearch ) {
	const q = ( s ) => encodeURIComponent( s );
	const mentions = new RegExp( `#${ number }\\b` );
	const commits = ( await gh( `search/commits?q=${ q( `repo:WordPress/wordpress-develop "#${ number }"` ) }&per_page=10` ) ).items
		.filter( ( c ) => mentions.test( c.commit.message ) )
		.map( ( c ) => ( { sha: c.sha, subject: c.commit.message.split( '\n' )[ 0 ], url: c.html_url } ) );
	const prs = ( await gh( `search/issues?q=${ q( `repo:WordPress/wordpress-develop is:pr "core.trac.wordpress.org/ticket/${ number }"` ) }&per_page=10` ) ).items
		.map( ( p ) => ( { number: p.number, title: p.title, state: p.state, url: p.html_url } ) );
	return { commits, prs };
}

export async function pool( items, size, fn ) {
	const out = [];
	let i = 0;
	await Promise.all( Array.from( { length: size }, async () => {
		while ( i < items.length ) {
			const idx = i++;
			out[ idx ] = await fn( items[ idx ] );
		}
	} ) );
	return out;
}
