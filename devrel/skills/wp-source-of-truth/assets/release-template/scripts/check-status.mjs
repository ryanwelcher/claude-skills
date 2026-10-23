#!/usr/bin/env node
// Looks up every GitHub PR/issue and Trac ticket linked from the post, plus release
// signals (latest Gutenberg releases, dev notes, Make Core posts for this release).
// Writes notes/status.json, plus notes/status-report.md with what changed since the previous run.
//
//   node scripts/check-status.mjs            # post only
//   node scripts/check-status.mjs --all      # post, notes and proposals
//
// GitHub lookups use `gh api` when gh is signed in, otherwise GITHUB_TOKEN, otherwise
// anonymous requests (60/hour, not enough for a full release).

import { readFileSync, readdirSync, statSync, writeFileSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';
import { execFileSync } from 'node:child_process';

const ROOT = new URL( '..', import.meta.url ).pathname;
const release = JSON.parse( readFileSync( join( ROOT, 'sot.json' ), 'utf8' ) );
const dirs = process.argv.includes( '--all' ) ? [ 'content', 'notes', 'proposals' ] : [ 'content' ];
const OUT = join( ROOT, 'notes', 'status.json' );

function walk( dir ) {
	if ( ! existsSync( dir ) ) return [];
	return readdirSync( dir ).flatMap( ( f ) => {
		const p = join( dir, f );
		return statSync( p ).isDirectory() ? walk( p ) : p.endsWith( '.md' ) ? [ p ] : [];
	} );
}

// ref key -> { kind, repo?, number, files: Set }
const refs = new Map();
for ( const file of dirs.flatMap( ( d ) => walk( join( ROOT, d ) ) ) ) {
	const src = readFileSync( file, 'utf8' );
	const rel = relative( ROOT, file );
	for ( const m of src.matchAll( /github\.com\/([\w.-]+\/[\w.-]+)\/(pull|issues)\/(\d+)/g ) ) {
		const key = `${ m[ 1 ] }#${ m[ 3 ] }`;
		if ( ! refs.has( key ) ) refs.set( key, { kind: 'github', repo: m[ 1 ], number: +m[ 3 ], files: new Set() } );
		refs.get( key ).files.add( rel );
	}
	for ( const m of src.matchAll( /core\.trac\.wordpress\.org\/ticket\/(\d+)/g ) ) {
		const key = `trac#${ m[ 1 ] }`;
		if ( ! refs.has( key ) ) refs.set( key, { kind: 'trac', number: +m[ 1 ], files: new Set() } );
		refs.get( key ).files.add( rel );
	}
}

let ghCli = false;
try {
	execFileSync( 'gh', [ 'auth', 'status' ], { stdio: 'ignore' } );
	ghCli = true;
} catch {}

async function github( path ) {
	if ( ghCli ) return JSON.parse( execFileSync( 'gh', [ 'api', path ], { encoding: 'utf8', maxBuffer: 1 << 24 } ) );
	const headers = { Accept: 'application/vnd.github+json', 'User-Agent': 'sot-check-status' };
	if ( process.env.GITHUB_TOKEN ) headers.Authorization = `Bearer ${ process.env.GITHUB_TOKEN }`;
	const res = await fetch( `https://api.github.com/${ path }`, { headers } );
	if ( ! res.ok ) throw new Error( `${ res.status } ${ path }` );
	return res.json();
}

function parseCsv( text ) {
	const rows = [];
	let row = [], cell = '', quoted = false;
	for ( let i = 0; i < text.length; i++ ) {
		const c = text[ i ];
		if ( quoted ) {
			if ( c === '"' && text[ i + 1 ] === '"' ) { cell += '"'; i++; }
			else if ( c === '"' ) quoted = false;
			else cell += c;
		} else if ( c === '"' ) quoted = true;
		else if ( c === ',' ) { row.push( cell ); cell = ''; }
		else if ( c === '\n' || c === '\r' ) {
			if ( c === '\r' && text[ i + 1 ] === '\n' ) i++;
			row.push( cell ); rows.push( row ); row = []; cell = '';
		} else cell += c;
	}
	if ( cell || row.length ) { row.push( cell ); rows.push( row ); }
	return rows;
}

async function lookup( ref ) {
	try {
		if ( ref.kind === 'github' ) {
			const d = await github( `repos/${ ref.repo }/issues/${ ref.number }` );
			const isPr = !! d.pull_request;
			return {
				type: isPr ? 'pr' : 'issue',
				title: d.title,
				state: isPr && d.pull_request.merged_at ? 'merged' : d.state,
				merged_at: d.pull_request?.merged_at ?? null,
				closed_at: d.closed_at,
				milestone: d.milestone?.title ?? null,
				labels: d.labels.map( ( l ) => l.name ).filter( ( n ) => /backport|wp |\[type\]|punt|needs dev note|has dev note/i.test( n ) ),
				draft: d.draft ?? false,
			};
		}
		const res = await fetch( `https://core.trac.wordpress.org/ticket/${ ref.number }?format=csv`, { headers: { 'User-Agent': 'sot-check-status' } } );
		// Trac usually answers scripts with a JavaScript browser check (403).
		if ( ! res.ok ) return await tracViaGithub( ref.number );
		const [ head, values ] = parseCsv( await res.text() );
		const t = Object.fromEntries( head.map( ( h, i ) => [ h.replace( /^﻿/, '' ), values?.[ i ] ] ) );
		return {
			type: 'trac',
			title: t.summary,
			state: t.resolution ? `${ t.status }/${ t.resolution }` : t.status,
			milestone: t.milestone,
			keywords: t.keywords,
			changed: t.changetime ?? t._changetime ?? null,
		};
	} catch ( e ) {
		return { error: String( e.message || e ) };
	}
}

// Core commits are mirrored to WordPress/wordpress-develop with "Fixes #N" / "See #N" in the
// message, and patches live there as PRs, so GitHub search stands in for Trac.
const sleep = ( ms ) => new Promise( ( r ) => setTimeout( r, ms ) );
let lastSearch = 0;
async function search( kind, q ) {
	// The search API allows 30 requests a minute.
	const wait = lastSearch + 2100 - Date.now();
	lastSearch = Date.now() + Math.max( wait, 0 );
	if ( wait > 0 ) await sleep( wait );
	const path = `search/${ kind }?q=${ encodeURIComponent( q ) }&per_page=10`;
	try {
		return await github( path );
	} catch {
		// Secondary rate limit: wait a minute and try once more.
		await sleep( 61000 );
		return github( path );
	}
}

async function tracViaGithub( number ) {
	const commits = ( await search( 'commits', `repo:WordPress/wordpress-develop "#${ number }"` ) ).items
		.filter( ( c ) => new RegExp( `#${ number }\\b` ).test( c.commit.message ) )
		.map( ( c ) => ( {
			date: c.commit.committer.date.slice( 0, 10 ),
			subject: c.commit.message.split( '\n' )[ 0 ],
			fixes: new RegExp( `Fixes #${ number }\\b` ).test( c.commit.message ),
			sha: c.sha.slice( 0, 10 ),
		} ) );
	const prs = ( await search( 'issues', `repo:WordPress/wordpress-develop is:pr "${ number }"` ) ).items
		.map( ( p ) => ( { number: p.number, state: p.state, title: p.title } ) );
	const fixed = commits.find( ( c ) => c.fixes );
	return {
		type: 'trac',
		source: 'github-mirror',
		state: fixed ? 'fixed' : commits.length ? 'commits' : prs.some( ( p ) => p.state === 'open' ) ? 'patch-open' : 'no-activity',
		milestone: null,
		last_commit: commits[ 0 ]?.date ?? null,
		commits,
		prs,
	};
}

async function pool( items, size, fn ) {
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

async function feedTitles( url ) {
	try {
		const res = await fetch( url, { headers: { 'User-Agent': 'sot-check-status' } } );
		if ( ! res.ok ) return { error: `${ res.status }` };
		const xml = await res.text();
		return [ ...xml.matchAll( /<item>[\s\S]*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/title>[\s\S]*?<link>(.*?)<\/link>[\s\S]*?<pubDate>(.*?)<\/pubDate>/g ) ]
			.map( ( m ) => ( { title: m[ 1 ], link: m[ 2 ], date: new Date( m[ 3 ] ).toISOString().slice( 0, 10 ) } ) );
	} catch ( e ) {
		return { error: String( e.message || e ) };
	}
}

const tag = release.version.replace( '.', '-' );
const entries = [ ...refs.entries() ];
// Trac refs go one at a time because their fallback uses the rate-limited search API.
const results = await pool( entries, ghCli ? 6 : 10, ( [ , ref ] ) => ( ref.kind === 'github' ? lookup( ref ) : null ) );
for ( const [ i, [ , ref ] ] of entries.entries() ) {
	if ( ref.kind === 'trac' ) results[ i ] = await lookup( ref );
}

const status = {
	checked_at: new Date().toISOString(),
	release: release.version,
	refs: Object.fromEntries( entries.map( ( [ key, ref ], i ) => [ key, { ...results[ i ], files: [ ...ref.files ].sort() } ] ) ),
	signals: {
		gutenberg_releases: await github( 'repos/WordPress/gutenberg/releases?per_page=6' )
			.then( ( rs ) => rs.map( ( r ) => ( { tag: r.tag_name, date: r.published_at?.slice( 0, 10 ), prerelease: r.prerelease } ) ) )
			.catch( ( e ) => ( { error: String( e.message ) } ) ),
		dev_notes: await feedTitles( `https://make.wordpress.org/core/tag/dev-notes+${ tag }/feed/` ),
		release_posts: await feedTitles( `https://make.wordpress.org/core/tag/${ tag }/feed/` ),
	},
};

const previous = existsSync( OUT ) ? JSON.parse( readFileSync( OUT, 'utf8' ) ) : null;
writeFileSync( OUT, JSON.stringify( status, null, '\t' ) + '\n' );

const fields = [ 'state', 'milestone', 'draft', 'last_commit' ];
const changes = [];
for ( const [ key, now ] of Object.entries( status.refs ) ) {
	const before = previous?.refs?.[ key ];
	if ( ! before ) {
		changes.push( `NEW   ${ key } ${ now.error ? `ERROR ${ now.error }` : `${ now.state } (${ now.milestone ?? 'no milestone' })` } — ${ now.files.join( ', ' ) }` );
		continue;
	}
	const diff = fields.filter( ( f ) => JSON.stringify( before[ f ] ) !== JSON.stringify( now[ f ] ) );
	if ( diff.length ) changes.push( `CHANGED ${ key } ${ diff.map( ( f ) => `${ f }: ${ before[ f ] } → ${ now[ f ] }` ).join( '; ' ) } — ${ now.files.join( ', ' ) }` );
}
const seenNotes = new Set( Array.isArray( previous?.signals?.dev_notes ) ? previous.signals.dev_notes.map( ( n ) => n.link ) : [] );
const newNotes = Array.isArray( status.signals.dev_notes ) ? status.signals.dev_notes.filter( ( n ) => ! seenNotes.has( n.link ) ) : [];
const errors = Object.entries( status.refs ).filter( ( [ , r ] ) => r.error );

const report = [];
report.push( `Checked ${ entries.length } refs (${ ghCli ? 'gh cli' : process.env.GITHUB_TOKEN ? 'GITHUB_TOKEN' : 'anonymous GitHub' }). Previous run: ${ previous?.checked_at ?? 'none' }` );
report.push( `\n## Ref changes (${ changes.length })\n${ changes.join( '\n' ) || '(none)' }` );
report.push( `\n## Open, unmerged PRs in the post\n${ Object.entries( status.refs ).filter( ( [ , r ] ) => r.type === 'pr' && r.state === 'open' ).map( ( [ k, r ] ) => `${ k } ${ r.draft ? '[draft] ' : '' }${ r.title } — ${ r.files.join( ', ' ) }` ).join( '\n' ) || '(none)' }` );
report.push( `\n## Trac tickets\n${ Object.entries( status.refs ).filter( ( [ , r ] ) => r.type === 'trac' ).map( ( [ k, r ] ) => `${ k } ${ r.state }${ r.milestone ? ` (${ r.milestone })` : '' }${ r.commits?.length ? ` — last commit ${ r.last_commit }: ${ r.commits[ 0 ].subject }` : '' }${ r.prs?.length ? ` — PRs ${ r.prs.map( ( p ) => `#${ p.number } ${ p.state }` ).join( ', ' ) }` : '' }` ).join( '\n' ) || '(none)' }` );
report.push( `\n## New dev notes (${ newNotes.length })\n${ newNotes.map( ( n ) => `${ n.date } ${ n.title } ${ n.link }` ).join( '\n' ) || '(none)' }` );
report.push( `\n## Latest Gutenberg releases\n${ Array.isArray( status.signals.gutenberg_releases ) ? status.signals.gutenberg_releases.map( ( r ) => `${ r.tag } ${ r.date }${ r.prerelease ? ' (RC)' : '' }` ).join( '\n' ) : JSON.stringify( status.signals.gutenberg_releases ) }` );
if ( errors.length ) report.push( `\n## Lookup errors (${ errors.length }) — check these by hand\n${ errors.map( ( [ k, r ] ) => `${ k } ${ r.error }` ).join( '\n' ) }` );

const text = report.join( '\n' ) + '\n';
writeFileSync( join( ROOT, 'notes', 'status-report.md' ), `# Status report\n\n${ text }` );
process.stdout.write( text );
