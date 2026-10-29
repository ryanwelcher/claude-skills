import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lookupGithub, lookupDevnote, tracViaGithub, pool } from '../lib/lookup.mjs';

const pr = { key: 'WordPress/gutenberg#81234', kind: 'github', repo: 'WordPress/gutenberg', number: 81234, url: 'https://github.com/WordPress/gutenberg/pull/81234' };
const gh = ( body ) => async () => body;

test( 'a merged PR reads as merged', async () => {
	const snap = await lookupGithub( pr, gh( { title: 'Notes', state: 'closed', pull_request: { merged_at: '2026-10-20T00:00:00Z' } } ) );
	assert.deepEqual( snap, { title: 'Notes', state: 'merged' } );
} );

test( 'a closed PR without a merge reads as closed', async () => {
	const snap = await lookupGithub( pr, gh( { title: 'Notes', state: 'closed', pull_request: { merged_at: null } } ) );
	assert.equal( snap.state, 'closed' );
} );

test( 'an issue keeps its state and milestone', async () => {
	const snap = await lookupGithub( { ...pr, url: 'https://github.com/WordPress/gutenberg/issues/81234' }, gh( { title: 'Tracking', state: 'open', milestone: { title: 'Gutenberg 24.4' } } ) );
	assert.deepEqual( snap, { title: 'Tracking', state: 'open', milestone: 'Gutenberg 24.4' } );
} );

test( 'a failed GitHub lookup returns an error snapshot', async () => {
	const snap = await lookupGithub( pr, async () => { throw new Error( '502 Bad Gateway' ); } );
	assert.equal( snap.state, 'unknown' );
	assert.match( snap.error, /502/ );
} );

const note = { key: 'url:https://make.wordpress.org/core/2026/10/20/x/', kind: 'devnote', url: 'https://make.wordpress.org/core/2026/10/20/x/' };

test( 'a dev note that answers is ok, with its page title', async () => {
	const snap = await lookupDevnote( note, async () => ( { ok: true, status: 200, text: async () => '<html><title>Block Bindings in 7.2 &#8211; Make WordPress Core</title></html>' } ) );
	assert.deepEqual( snap, { title: 'Block Bindings in 7.2', state: 'ok' } );
} );

test( 'a dev note that 404s is missing', async () => {
	const snap = await lookupDevnote( note, async () => ( { ok: false, status: 404, text: async () => '' } ) );
	assert.equal( snap.state, 'missing' );
} );

test( 'Trac via GitHub searches commits and PRs that mention the ticket', async () => {
	const paths = [];
	const stub = async ( path ) => {
		paths.push( decodeURIComponent( path ) );
		if ( path.startsWith( 'search/commits' ) ) return { items: [
			{ sha: '92c17418abcdef', html_url: 'https://github.com/WordPress/wordpress-develop/commit/92c17418abcdef', commit: { message: 'Security: Keep the previous secret version.\n\nFixes #66187.' } },
			{ sha: 'aaaa', html_url: 'u', commit: { message: 'Unrelated #661870' } },
		] };
		return { items: [ { number: 15124, title: 'Generate WP_SECRETS_KEY', state: 'open', html_url: 'https://github.com/WordPress/wordpress-develop/pull/15124' } ] };
	};
	const r = await tracViaGithub( 66187, stub );
	assert.ok( paths[ 0 ].startsWith( 'search/commits?q=repo:WordPress/wordpress-develop "#66187"' ) );
	assert.ok( paths[ 1 ].startsWith( 'search/issues?q=repo:WordPress/wordpress-develop is:pr "core.trac.wordpress.org/ticket/66187"' ) );
	assert.deepEqual( r.commits, [ { sha: '92c17418abcdef', subject: 'Security: Keep the previous secret version.', url: 'https://github.com/WordPress/wordpress-develop/commit/92c17418abcdef' } ] );
	assert.deepEqual( r.prs, [ { number: 15124, title: 'Generate WP_SECRETS_KEY', state: 'open', url: 'https://github.com/WordPress/wordpress-develop/pull/15124' } ] );
} );

test( 'pool keeps results in input order', async () => {
	const out = await pool( [ 3, 1, 2 ], 2, async ( n ) => { await new Promise( ( r ) => setTimeout( r, n ) ); return n * 10; } );
	assert.deepEqual( out, [ 30, 10, 20 ] );
} );
