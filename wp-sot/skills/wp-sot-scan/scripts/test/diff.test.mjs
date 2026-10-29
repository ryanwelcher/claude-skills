import { test } from 'node:test';
import assert from 'node:assert/strict';
import { diffRefs, tracFindings } from '../lib/diff.mjs';

const pr = { key: 'WordPress/gutenberg#1', kind: 'github', repo: 'WordPress/gutenberg', number: 1, url: 'https://github.com/WordPress/gutenberg/pull/1' };
const issue = { key: 'WordPress/gutenberg#2', kind: 'github', repo: 'WordPress/gutenberg', number: 2, url: 'https://github.com/WordPress/gutenberg/issues/2' };
const note = { key: 'url:https://make.wordpress.org/core/x/', kind: 'devnote', url: 'https://make.wordpress.org/core/x/' };
const texts = ( findings ) => findings.map( ( f ) => f.text );

test( 'GitHub state changes become findings', () => {
	const prev = { [ pr.key ]: { title: 'Notes', state: 'open' }, [ issue.key ]: { title: 'Tracking', state: 'closed' } };
	const curr = { [ pr.key ]: { title: 'Notes', state: 'merged' }, [ issue.key ]: { title: 'Tracking', state: 'open' } };
	const f = diffRefs( prev, curr, [ pr, issue ] );
	assert.deepEqual( texts( f ), [ 'Merged: Notes.', 'Reopened: Tracking.' ] );
	assert.deepEqual( f[ 0 ], { group: 'changes', text: 'Merged: Notes.', url: pr.url, key: pr.key } );
} );

test( 'a PR closed without merging, and a closed issue', () => {
	const prev = { [ pr.key ]: { title: 'A', state: 'open' }, [ issue.key ]: { title: 'B', state: 'open' } };
	const curr = { [ pr.key ]: { title: 'A', state: 'closed' }, [ issue.key ]: { title: 'B', state: 'closed' } };
	assert.deepEqual( texts( diffRefs( prev, curr, [ pr, issue ] ) ), [ 'Closed without merging: A.', 'Closed: B.' ] );
} );

test( 'a dev note that disappears is a broken link', () => {
	const f = diffRefs( { [ note.key ]: { title: 'Bindings', state: 'ok' } }, { [ note.key ]: { title: '', state: 'missing' } }, [ note ] );
	assert.deepEqual( texts( f ), [ 'Link broken: Bindings.' ] );
} );

test( 'the first run and failed lookups report nothing', () => {
	assert.deepEqual( diffRefs( null, { [ pr.key ]: { title: 'A', state: 'merged' } }, [ pr ] ), [] );
	assert.deepEqual( diffRefs( { [ pr.key ]: { title: 'A', state: 'open' } }, { [ pr.key ]: { title: '', state: 'unknown', error: '502' } }, [ pr ] ), [] );
} );

const linked = new Set( [ 'trac#61234', 'trac#66187', 'trac#66408' ] );
const prevTrac = {
	'trac#61234': { title: 'Font Library uploads', state: 'assigned', milestone: '7.2' },
	'trac#66187': { title: 'Secrets API', state: 'closed/fixed', milestone: '7.2' },
	'trac#66408': { title: 'PclZip', state: 'new', milestone: '7.2' },
};

test( 'with the CSV: milestone moves, closes and reopens', () => {
	const csvRows = [
		{ id: 61234, summary: 'Font Library uploads', status: 'assigned', resolution: '', milestone: '7.3', keywords: '' },
		{ id: 66187, summary: 'Secrets API', status: 'reopened', resolution: '', milestone: '7.2', keywords: '' },
		{ id: 66408, summary: 'PclZip', status: 'closed', resolution: 'wontfix', milestone: '7.2', keywords: '' },
	];
	const { findings, snapshots } = tracFindings( { linked, events: [ { ticket: 66408, kind: 'reopened', fields: [], title: 'PclZip', link: '', date: '' } ], csvRows, prev: prevTrac, milestone: '7.2', ghTrac: {} } );
	assert.deepEqual( texts( findings ).sort(), [ 'Closed (wontfix): #66408 PclZip.', 'Moved to 7.3: #61234 Font Library uploads.', 'Reopened: #66187 Secrets API.' ] );
	assert.ok( findings.every( ( f ) => f.url.startsWith( 'https://core.trac.wordpress.org/ticket/' ) && f.group === 'changes' ) );
	assert.equal( snapshots[ 'trac#61234' ].milestone, '7.3' );
	assert.equal( snapshots[ 'trac#66408' ].state, 'closed/wontfix' );
} );

test( 'with the CSV: unlinked tickets on the milestone that are new are listed for Pass 2', () => {
	const csvRows = [ { id: 70000, summary: 'Brand new', status: 'new', resolution: '', milestone: '7.2', keywords: '' }, { id: 70001, summary: 'Old news', status: 'new', resolution: '', milestone: '7.2', keywords: '' } ];
	const prev = { ...prevTrac, 'trac#70001': { title: 'Old news', state: 'new', milestone: '7.2' } };
	const r = tracFindings( { linked, events: [], csvRows, prev, milestone: '7.2', ghTrac: {} } );
	assert.deepEqual( r.findings, [] );
	assert.deepEqual( r.newTickets, [ { number: 70000, summary: 'Brand new', url: 'https://core.trac.wordpress.org/ticket/70000' } ] );
	assert.ok( r.snapshots[ 'trac#70000' ] );
} );

test( 'without the CSV: timeline events for linked tickets', () => {
	const events = [
		{ ticket: 61234, kind: 'updated', fields: [ 'milestone' ], title: 'Font Library uploads', link: '', date: '2026-10-23' },
		{ ticket: 66187, kind: 'reopened', fields: [], title: 'Secrets API', link: '', date: '2026-10-22' },
		{ ticket: 66408, kind: 'closed', resolution: 'fixed', fields: [], title: 'PclZip', link: '', date: '2026-10-22' },
		{ ticket: 99999, kind: 'closed', resolution: 'fixed', fields: [], title: 'Not linked', link: '', date: '2026-10-22' },
	];
	const { findings } = tracFindings( { linked, events, csvRows: null, prev: prevTrac, milestone: '7.2', ghTrac: {} } );
	assert.deepEqual( texts( findings ).sort(), [ 'Closed (fixed): #66408 PclZip.', 'Milestone changed on #61234 Font Library uploads, check whether it was punted.', 'Reopened: #66187 Secrets API.' ] );
} );

test( 'a new commit on a linked ticket is reported, unless the ticket also closed', () => {
	const prev = { 'trac#61234': { ...prevTrac[ 'trac#61234' ], commits: 1 }, 'trac#66408': { ...prevTrac[ 'trac#66408' ], commits: 0 } };
	const ghTrac = {
		61234: { commits: [ { sha: 'b', subject: 'Fonts: second fix.', url: 'https://github.com/WordPress/wordpress-develop/commit/b' }, { sha: 'a', subject: 'first', url: 'x' } ], prs: [] },
		66408: { commits: [ { sha: 'c', subject: 'Fix PclZip.', url: 'y' } ], prs: [] },
	};
	const events = [ { ticket: 66408, kind: 'closed', resolution: 'fixed', fields: [], title: 'PclZip', link: '', date: '' } ];
	const { findings, snapshots } = tracFindings( { linked, events, csvRows: null, prev, milestone: '7.2', ghTrac } );
	assert.deepEqual( texts( findings ).sort(), [ 'Closed (fixed): #66408 PclZip.', 'Committed: #61234 Fonts: second fix.' ] );
	assert.equal( findings.find( ( f ) => f.text.startsWith( 'Committed' ) ).url, 'https://github.com/WordPress/wordpress-develop/commit/b' );
	assert.equal( snapshots[ 'trac#61234' ].commits, 2 );
} );

test( 'the first run reports timeline events but not commits', () => {
	const ghTrac = { 61234: { commits: [ { sha: 'b', subject: 's', url: 'u' } ], prs: [] } };
	const events = [ { ticket: 66187, kind: 'reopened', fields: [], title: 'Secrets API', link: '', date: '' } ];
	const { findings } = tracFindings( { linked, events, csvRows: null, prev: null, milestone: '7.2', ghTrac } );
	assert.deepEqual( texts( findings ), [ 'Reopened: #66187 Secrets API.' ] );
} );

test( 'no finding text has an em-dash', () => {
	const csvRows = [ { id: 61234, summary: 'Fonts — part two', status: 'assigned', resolution: '', milestone: '7.3', keywords: '' } ];
	const { findings } = tracFindings( { linked, events: [], csvRows, prev: prevTrac, milestone: '7.2', ghTrac: {} } );
	assert.equal( findings.length, 1 );
	assert.ok( ! findings[ 0 ].text.includes( '—' ) );
} );
