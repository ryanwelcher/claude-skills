import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseTimeline, fetchTimeline, parseQueryCsv } from '../lib/trac.mjs';

const xml = readFileSync( new URL( 'fixtures/timeline.xml', import.meta.url ), 'utf8' );
const csv = readFileSync( new URL( 'fixtures/query.csv', import.meta.url ), 'utf8' );

test( 'parses each kind of timeline event', () => {
	const events = parseTimeline( xml );
	assert.equal( events.length, 7 );
	const closed = events.find( ( e ) => e.kind === 'closed' );
	assert.equal( closed.ticket, 66408 );
	assert.equal( closed.resolution, 'fixed' );
	const updated = events.find( ( e ) => e.kind === 'updated' );
	assert.deepEqual( updated.fields, [ 'milestone' ] );
	const cs = events.find( ( e ) => e.kind === 'changeset' );
	assert.equal( cs.changeset, 65003 );
	assert.equal( cs.ticket, null );
	assert.equal( events.find( ( e ) => e.kind === 'reopened' ).ticket, 66187 );
	assert.equal( events[ 0 ].date, '2026-10-22' );
	assert.equal( events[ 0 ].title, 'register_block_type_from_metadata performs unneccesary file system ...' );
} );

// Trac returns the "from" day and the day before it, whatever daysback says below 1.
const item = ( day, n ) => `<item><title>Ticket #${ n } (T${ n }) created</title><link>https://core.trac.wordpress.org/ticket/${ n }</link><pubDate>${ day } GMT</pubDate><description></description></item>`;
function stubTrac( calls ) {
	const byDay = { '10/22/26': 'Thu, 22 Oct 2026 12:00:00', '10/23/26': 'Fri, 23 Oct 2026 12:00:00', '10/24/26': 'Sat, 24 Oct 2026 12:00:00', '10/25/26': 'Sun, 25 Oct 2026 12:00:00', '10/21/26': 'Wed, 21 Oct 2026 12:00:00' };
	const prev = { '10/23/26': '10/22/26', '10/25/26': '10/24/26', '10/22/26': '10/21/26', '10/24/26': '10/23/26' };
	return async ( url ) => {
		calls.push( url );
		const from = new URL( url ).searchParams.get( 'from' );
		const days = [ from, prev[ from ] ];
		const body = `<rss><channel>${ days.map( ( d, i ) => item( byDay[ d ], 1000 + Object.keys( byDay ).indexOf( d ) ) ).join( '' ) }</channel></rss>`;
		return { ok: true, text: async () => body };
	};
}

test( 'fetches two days per request and keeps only the requested days', async () => {
	const calls = [];
	const events = await fetchTimeline( new Date( '2026-10-22T00:00:00Z' ), 3, stubTrac( calls ) );
	assert.equal( calls.length, 2 );
	assert.ok( calls.every( ( u ) => u.includes( 'daysback=1' ) && u.includes( 'max=5000' ) && u.includes( 'ticket_details=on' ) ) );
	assert.deepEqual( calls.map( ( u ) => new URL( u ).searchParams.get( 'from' ) ), [ '10/23/26', '10/25/26' ] );
	assert.deepEqual( events.map( ( e ) => e.date ).sort(), [ '2026-10-22', '2026-10-23', '2026-10-24' ] );
} );

test( 'splits a batch update into one event per ticket', () => {
	const batch = parseTimeline( xml ).filter( ( e ) => e.title === '' );
	assert.deepEqual( batch.map( ( e ) => e.ticket ), [ 66187, 66353 ] );
	assert.ok( batch.every( ( e ) => e.kind === 'closed' && e.resolution === 'fixed' ) );
	assert.equal( batch[ 0 ].link, 'https://core.trac.wordpress.org/ticket/66187' );
} );

test( 'parses the query CSV, BOM and quoted commas included', () => {
	const rows = parseQueryCsv( csv );
	assert.equal( rows.length, 2 );
	assert.deepEqual( rows[ 0 ], { id: 61234, summary: 'Font Library: uploads, part two', status: 'assigned', milestone: '7.3', keywords: 'has-patch' } );
} );
