import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderBlock } from '../lib/block.mjs';

const findings = [
	{ group: 'changes', text: 'Reopened: #66187 Secrets API.', url: 'https://core.trac.wordpress.org/ticket/66187' },
	{ group: 'candidates', text: 'Tabs block.', url: 'https://github.com/WordPress/gutenberg/pull/81999' },
];

test( 'heading, checked line, notes, groups and footer in order', () => {
	const { markdown } = renderBlock( { date: '2026-10-29', checked: '26 linked tickets and PRs, 312 Gutenberg PRs', notes: [ 'First scan for this release, so changes to linked items start next week.' ], findings } );
	const lines = markdown.split( '\n' ).filter( Boolean );
	assert.equal( lines[ 0 ], '## Automated scan results: October 29, 2026' );
	assert.equal( lines[ 1 ], 'Checked 26 linked tickets and PRs, 312 Gutenberg PRs.' );
	assert.equal( lines[ 2 ], 'First scan for this release, so changes to linked items start next week.' );
	assert.equal( lines[ 3 ], 'Changes to linked items' );
	assert.equal( lines[ 4 ], '- Reopened: #66187 Secrets API. https://core.trac.wordpress.org/ticket/66187' );
	assert.equal( lines[ 5 ], 'New candidates (not in the Doc yet)' );
	assert.equal( lines[ 6 ], '- Tabs block. https://github.com/WordPress/gutenberg/pull/81999' );
	assert.equal( lines.at( -1 ), 'End of automated scan results: October 29, 2026' );
} );

test( 'empty groups say so', () => {
	const { markdown } = renderBlock( { date: '2026-10-29', checked: 'x', notes: [], findings: [] } );
	assert.ok( markdown.includes( 'No changes to linked items' ) );
	assert.ok( markdown.includes( 'No new candidates' ) );
} );

test( 'the HTML has a real heading, list items and clickable links', () => {
	const { html } = renderBlock( { date: '2026-10-29', checked: 'x', notes: [], findings } );
	assert.ok( html.includes( '<h2>Automated scan results: October 29, 2026</h2>' ) );
	assert.ok( html.includes( '<p>Changes to linked items</p>' ) );
	assert.ok( html.includes( '<li>Reopened: #66187 Secrets API. <a href="https://core.trac.wordpress.org/ticket/66187">https://core.trac.wordpress.org/ticket/66187</a></li>' ) );
	assert.ok( html.includes( '<p>End of automated scan results: October 29, 2026</p>' ) );
} );

test( 'HTML escapes text from tickets', () => {
	const { html } = renderBlock( { date: '2026-10-29', checked: 'x', notes: [], findings: [ { group: 'changes', text: 'Merged: <script> & co.', url: 'https://github.com/a/b/pull/1' } ] } );
	assert.ok( html.includes( 'Merged: &lt;script&gt; &amp; co.' ) );
} );

test( 'no em-dashes in either output', () => {
	const { markdown, html } = renderBlock( { date: '2026-10-29', checked: 'a — b', notes: [ 'c — d' ], findings: [ { group: 'changes', text: 'e — f.', url: 'https://x.y/' } ] } );
	assert.ok( ! markdown.includes( '—' ) && ! html.includes( '—' ) );
} );
