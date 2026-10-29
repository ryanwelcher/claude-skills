import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { finish } from '../finish.mjs';

const PR = ( n ) => `https://github.com/WordPress/gutenberg/pull/${ n }`;
const KEY = ( n ) => `WordPress/gutenberg#${ n }`;

function setup( work, candidates ) {
	const root = mkdtempSync( join( tmpdir(), 'finish-' ) );
	const releaseDir = join( root, '7.2' );
	mkdirSync( join( releaseDir, 'notes' ), { recursive: true } );
	const base = { date: '2026-10-29', version: '7.2', tab: 'Notes', firstRun: false, tracCsv: true, docKeys: [], struckKeys: [], findings: [], snapshots: { a: { title: 'A', state: 'open' } }, newTickets: [], openCandidates: [], checked: { linked: 26 } };
	writeFileSync( join( root, 'work.json' ), JSON.stringify( { ...base, ...work } ) );
	writeFileSync( join( root, 'candidates.json' ), JSON.stringify( { checked: '312 Gutenberg PRs', items: [], ...candidates } ) );
	const copies = [];
	return { releaseDir, opts: { releaseDir, work: join( root, 'work.json' ), candidates: join( root, 'candidates.json' ) }, deps: { copy: async ( html, text ) => copies.push( { html, text } ) }, copies };
}

const cand = ( n ) => ( { group: 'candidates', text: `Item ${ n }.`, url: PR( n ) } );

test( 'candidates already in the Doc or struck out are dropped', async () => {
	const t = setup( { docKeys: [ KEY( 1 ) ], struckKeys: [ KEY( 2 ) ] }, { items: [ cand( 1 ), cand( 2 ), cand( 3 ) ] } );
	const { markdown } = await finish( t.opts, t.deps );
	assert.ok( ! markdown.includes( PR( 1 ) ) && ! markdown.includes( PR( 2 ) ) );
	assert.ok( markdown.includes( PR( 3 ) ) );
} );

test( 'a candidate that repeats a Pass 1 finding is dropped', async () => {
	const t = setup( { findings: [ { group: 'changes', text: 'Merged: Item 4.', url: PR( 4 ), key: KEY( 4 ) } ] }, { items: [ cand( 4 ) ] } );
	const { markdown } = await finish( t.opts, t.deps );
	assert.equal( markdown.split( PR( 4 ) ).length - 1, 1 );
} );

test( 'open candidates carry forward until added or struck', async () => {
	const open = [ { ...cand( 5 ), key: KEY( 5 ) }, { ...cand( 6 ), key: KEY( 6 ) }, { ...cand( 7 ), key: KEY( 7 ) } ];
	const t = setup( { openCandidates: open, docKeys: [ KEY( 6 ) ], struckKeys: [ KEY( 7 ) ] }, { items: [ cand( 5 ) ] } );
	const { markdown } = await finish( t.opts, t.deps );
	assert.equal( markdown.split( PR( 5 ) ).length - 1, 1 );
	assert.ok( ! markdown.includes( PR( 6 ) ) && ! markdown.includes( PR( 7 ) ) );
	const state = JSON.parse( readFileSync( join( t.releaseDir, 'notes', 'scan-state.json' ), 'utf8' ) );
	assert.deepEqual( state.openCandidates.map( ( c ) => c.key ), [ KEY( 5 ) ] );
} );

test( 'writes the scan file and the state', async () => {
	const t = setup( {}, { items: [ cand( 8 ) ] } );
	const { file, markdown } = await finish( t.opts, t.deps );
	assert.equal( file, join( t.releaseDir, 'notes', 'scans', '2026-10-29.md' ) );
	const saved = readFileSync( file, 'utf8' );
	assert.ok( saved.startsWith( '---\ntab: Notes\n---\n\n' ) );
	assert.ok( saved.endsWith( markdown ) );
	const state = JSON.parse( readFileSync( join( t.releaseDir, 'notes', 'scan-state.json' ), 'utf8' ) );
	assert.equal( state.lastRun, '2026-10-29' );
	assert.deepEqual( state.refs, { a: { title: 'A', state: 'open' } } );
	assert.ok( markdown.includes( 'Checked 26 linked tickets and PRs, 312 Gutenberg PRs.' ) );
} );

test( 'first-run and no-CSV notes', async () => {
	const t = setup( { firstRun: true, tracCsv: false }, {} );
	const { markdown } = await finish( t.opts, t.deps );
	assert.ok( markdown.includes( 'First scan for this release, so changes to linked items start next week.' ) );
	assert.ok( markdown.includes( "Trac milestone values weren't checked this week." ) );
} );

test( 'copies the HTML and Markdown once', async () => {
	const t = setup( {}, { items: [ cand( 9 ) ] } );
	const { markdown } = await finish( t.opts, t.deps );
	assert.equal( t.copies.length, 1 );
	assert.ok( t.copies[ 0 ].html.startsWith( '<h2>' ) );
	assert.equal( t.copies[ 0 ].text, markdown );
} );
