import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';
import { prepare } from '../prepare.mjs';

const fixture = new URL( 'fixtures/doc-72.md', import.meta.url ).pathname;
const PR = 'WordPress/gutenberg#84851';

function releaseDir( state ) {
	const dir = join( mkdtempSync( join( tmpdir(), 'scan-' ) ), '7.2' );
	mkdirSync( join( dir, 'notes' ), { recursive: true } );
	if ( state ) writeFileSync( join( dir, 'notes', 'scan-state.json' ), JSON.stringify( state ) );
	return dir;
}

function deps( calls = {} ) {
	return {
		lookupGithub: async ( ref ) => ( ref.key === PR ? { title: 'Auto-attach', state: 'merged' } : { title: 'x', state: 'open' } ),
		lookupDevnote: async () => ( { title: 'note', state: 'ok' } ),
		fetchTimeline: async ( from, days ) => {
			calls.timeline = { from: from.toISOString().slice( 0, 10 ), days };
			return [];
		},
		tracViaGithub: async () => ( { commits: [], prs: [] } ),
	};
}

test( 'an unknown tab stops the run and lists the real tabs', async () => {
	await assert.rejects( prepare( { releaseDir: releaseDir(), doc: fixture, tab: 'Scan Results', date: '2026-10-29' }, deps() ), /Notes/ );
} );

test( 'a Google sign-in page stops the run', async () => {
	const signin = join( mkdtempSync( join( tmpdir(), 'scan-' ) ), 'signin.md' );
	writeFileSync( signin, '<!DOCTYPE html><html><head><title>Sign in</title></head><body>accounts.google.com</body></html>' );
	await assert.rejects( prepare( { releaseDir: releaseDir(), doc: signin, date: '2026-10-29' }, deps() ), /sign-in/ );
} );

test( 'the first run records a baseline and reads the last 7 days of Trac', async () => {
	const calls = {};
	const work = await prepare( { releaseDir: releaseDir(), doc: fixture, date: '2026-10-29' }, deps( calls ) );
	assert.equal( work.firstRun, true );
	assert.deepEqual( work.findings, [] );
	assert.deepEqual( calls.timeline, { from: '2026-10-22', days: 7 } );
	assert.equal( work.snapshots[ PR ].state, 'merged' );
	assert.equal( work.tab, 'Notes' );
	assert.equal( work.version, '7.2' );
} );

test( 'a later run reports changes since lastRun', async () => {
	const calls = {};
	const state = { lastRun: '2026-10-22', refs: { [ PR ]: { title: 'Auto-attach', state: 'open' } }, openCandidates: [ { group: 'candidates', text: 'Font size presets.', url: 'https://github.com/WordPress/gutenberg/pull/81777', key: 'WordPress/gutenberg#81777' } ] };
	const work = await prepare( { releaseDir: releaseDir( state ), doc: fixture, date: '2026-10-29' }, deps( calls ) );
	assert.equal( work.firstRun, false );
	assert.deepEqual( work.findings.map( ( f ) => f.text ), [ 'Merged: Auto-attach.' ] );
	assert.deepEqual( calls.timeline, { from: '2026-10-22', days: 7 } );
	assert.equal( work.openCandidates.length, 1 );
} );

test( 'a long gap reads at most 31 days of Trac', async () => {
	const calls = {};
	await prepare( { releaseDir: releaseDir( { lastRun: '2026-08-01', refs: {}, openCandidates: [] } ), doc: fixture, date: '2026-10-29' }, deps( calls ) );
	assert.deepEqual( calls.timeline, { from: '2026-09-28', days: 31 } );
} );

test( 'doc keys come from human text only, struck keys from the blocks', async () => {
	const work = await prepare( { releaseDir: releaseDir(), doc: fixture, date: '2026-10-29' }, deps() );
	assert.ok( work.docKeys.includes( 'WordPress/gutenberg#81888' ) );
	assert.ok( ! work.docKeys.includes( 'WordPress/gutenberg#81777' ) );
	assert.deepEqual( work.struckKeys, [ 'WordPress/gutenberg#81500' ] );
	assert.equal( work.checked.linked, work.docKeys.filter( ( k ) => ! k.startsWith( 'url:' ) || k.includes( 'make.wordpress.org/core/' ) ).length );
	assert.equal( work.tracCsv, false );
} );

test( 'with both CSVs, Trac milestone values are used', async () => {
	const dir = mkdtempSync( join( tmpdir(), 'scan-' ) );
	const csv = 'id,summary,status,resolution,milestone,keywords\n66187,Secrets API,reopened,,7.2,\n70000,Brand new,new,,7.2,\n';
	writeFileSync( join( dir, 'linked.csv' ), csv );
	writeFileSync( join( dir, 'milestone.csv' ), csv );
	const work = await prepare( { releaseDir: releaseDir(), doc: fixture, date: '2026-10-29', tracLinked: join( dir, 'linked.csv' ), tracMilestone: join( dir, 'milestone.csv' ) }, deps() );
	assert.equal( work.tracCsv, true );
	assert.equal( work.snapshots[ 'trac#66187' ].milestone, '7.2' );
	assert.deepEqual( work.newTickets.map( ( t ) => t.number ), [ 70000 ] );
} );

test( '--list-trac prints linked ticket numbers from the human text', () => {
	const out = execFileSync( 'node', [ new URL( '../prepare.mjs', import.meta.url ).pathname, '--doc', fixture, '--list-trac' ], { encoding: 'utf8' } ).trim();
	const ids = out.split( ',' );
	assert.ok( ids.includes( '66187' ) );
	assert.ok( ids.every( ( id ) => /^\d+$/.test( id ) ) );
} );
