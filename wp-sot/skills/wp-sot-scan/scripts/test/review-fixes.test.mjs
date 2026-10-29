// Regression tests for the final review's findings.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { parseDoc, struckKeys } from '../lib/doc.mjs';
import { refKey, extractRefs } from '../lib/refs.mjs';
import { tracFindings } from '../lib/diff.mjs';
import { prepare } from '../prepare.mjs';
import { finish } from '../finish.mjs';

const CS = 'https://core.trac.wordpress.org/changeset/61234';

test( 'R1: any http(s) URL has a key, so it can be struck or found in the Doc', () => {
	assert.equal( refKey( CS ), `url:${ CS }` );
	assert.equal( refKey( 'https://make.wordpress.org/test/2026/10/01/call/?x=1#y' ), 'url:https://make.wordpress.org/test/2026/10/01/call' );
	assert.equal( refKey( 'https://make.wordpress.org/test/2026/10/01/call/' ), refKey( 'https://make.wordpress.org/test/2026/10/01/call' ) );
	const doc = parseDoc( `# **Notes**\n\n## Automated scan results: October 22, 2026\n\n* ~~Changeset. ${ CS }~~\n\nEnd of automated scan results: October 22, 2026\n` );
	assert.deepEqual( struckKeys( doc.blocks ), new Set( [ `url:${ CS }` ] ) );
	assert.ok( extractRefs( `see ${ CS }.` ).some( ( r ) => r.key === `url:${ CS }` ) );
} );

test( 'R2: striking only the words of a line still strikes its link', () => {
	const doc = parseDoc( '# **Notes**\n\n## Automated scan results: October 22, 2026\n\n* ~~Accordion block attributes.~~ [https://github.com/WordPress/gutenberg/pull/81500](https://github.com/WordPress/gutenberg/pull/81500)\n\nEnd of automated scan results: October 22, 2026\n' );
	assert.deepEqual( struckKeys( doc.blocks ), new Set( [ 'WordPress/gutenberg#81500' ] ) );
} );

test( 'R3: a block pasted as plain text is still found', () => {
	const doc = parseDoc( '# **Notes**\n\n\\#\\# Automated scan results: October 22, 2026\n\n\\- Tabs block. https://github.com/WordPress/gutenberg/pull/81999\n\nEnd of automated scan results: October 22, 2026\n\nmine https://github.com/WordPress/gutenberg/pull/1\n' );
	assert.equal( doc.blocks.length, 1 );
	assert.ok( ! doc.humanText.includes( '81999' ) );
	assert.ok( doc.humanText.includes( 'pull/1' ) );
} );

const linked = new Set( [ 'trac#66408' ] );

test( 'R4: the first run with the CSV still reports last week\'s timeline events', () => {
	const csvRows = [ { id: 66408, summary: 'PclZip', status: 'closed', resolution: 'fixed', milestone: '7.2', keywords: '' } ];
	const events = [ { ticket: 66408, kind: 'closed', resolution: 'fixed', fields: [], title: 'PclZip', link: '', date: '' } ];
	const { findings, snapshots } = tracFindings( { linked, events, csvRows, prev: null, milestone: '7.2', ghTrac: {} } );
	assert.deepEqual( findings.map( ( f ) => f.text ), [ 'Closed (fixed): #66408 PclZip.' ] );
	assert.equal( snapshots[ 'trac#66408' ].milestone, '7.2' );
} );

test( 'R5: an unknown baseline is not a baseline', () => {
	const csvRows = [ { id: 66408, summary: 'PclZip', status: 'closed', resolution: 'fixed', milestone: '7.2', keywords: '' } ];
	const prev = { 'trac#66408': { title: 'PclZip', state: 'unknown' } };
	assert.deepEqual( tracFindings( { linked, events: [], csvRows, prev, milestone: '7.2', ghTrac: {} } ).findings, [] );
} );

test( 'R5/R6: a failed tracViaGithub keeps the previous commit count', () => {
	const prev = { 'trac#66408': { title: 'PclZip', state: 'new', milestone: '7.2', commits: 3 } };
	const { snapshots } = tracFindings( { linked, events: [], csvRows: null, prev, milestone: '7.2', ghTrac: {} } );
	assert.equal( snapshots[ 'trac#66408' ].commits, 3 );
} );

const fixture = new URL( 'fixtures/doc-72.md', import.meta.url ).pathname;
const PR = 'WordPress/gutenberg#84851';
function relDir( state ) {
	const dir = join( mkdtempSync( join( tmpdir(), 'rf-' ) ), '7.2' );
	mkdirSync( join( dir, 'notes' ), { recursive: true } );
	if ( state ) writeFileSync( join( dir, 'notes', 'scan-state.json' ), JSON.stringify( state ) );
	return dir;
}
const deps = ( over = {} ) => ( {
	lookupGithub: async () => ( { title: 'x', state: 'open' } ),
	lookupDevnote: async () => ( { title: 'n', state: 'ok' } ),
	fetchTimeline: async () => [],
	tracViaGithub: async () => ( { commits: [], prs: [] } ),
	...over,
} );

test( 'R6: a failed lookup keeps last week\'s snapshot, and untouched refs carry forward', async () => {
	const state = { lastRun: '2026-10-22', refs: { [ PR ]: { title: 'Auto-attach', state: 'open' }, 'trac#70001': { title: 'Old', state: 'new', milestone: '7.2' } }, openCandidates: [] };
	const work = await prepare( { releaseDir: relDir( state ), doc: fixture, date: '2026-10-29' }, deps( { lookupGithub: async () => ( { title: '', state: 'unknown', error: '502' } ) } ) );
	assert.deepEqual( work.snapshots[ PR ], { title: 'Auto-attach', state: 'open' } );
	assert.ok( work.snapshots[ 'trac#70001' ] );
} );

test( 'R7: an unreachable Trac timeline is a note, not a stop', async () => {
	const work = await prepare( { releaseDir: relDir(), doc: fixture, date: '2026-10-29' }, deps( { fetchTimeline: async () => { throw new Error( 'Trac timeline returned 403' ); } } ) );
	assert.ok( work.notes.includes( "The Trac timeline wasn't reachable this week." ) );
} );

test( 'R7: work notes reach the block, and items without a link are skipped', async () => {
	const root = mkdtempSync( join( tmpdir(), 'rf-' ) );
	const releaseDir = join( root, '7.2' );
	mkdirSync( join( releaseDir, 'notes' ), { recursive: true } );
	writeFileSync( join( root, 'w.json' ), JSON.stringify( { date: '2026-10-29', version: '7.2', tab: 'Notes', firstRun: false, tracCsv: true, docKeys: [], struckKeys: [], findings: [], snapshots: {}, newTickets: [], openCandidates: [], checked: { linked: 1 }, notes: [ "The Trac timeline wasn't reachable this week." ] } ) );
	writeFileSync( join( root, 'c.json' ), JSON.stringify( { checked: 'x', items: [ { group: 'candidates', text: 'No link.' }, { group: 'candidates', text: 'Relative.', url: '/foo' }, { group: 'candidates', text: 'Good.', url: CS } ] } ) );
	const { markdown } = await finish( { releaseDir, work: join( root, 'w.json' ), candidates: join( root, 'c.json' ) }, { copy: async () => true } );
	assert.ok( markdown.includes( "The Trac timeline wasn't reachable this week." ) );
	assert.ok( ! markdown.includes( 'undefined' ) && ! markdown.includes( 'No link.' ) && ! markdown.includes( 'Relative.' ) );
	assert.ok( markdown.includes( `Good. ${ CS }` ) );
} );
