// Trac data the scan can read. Only the timeline RSS feed answers scripted requests; query CSVs
// come from Justin's own Chrome and are parsed here.

const TIMELINE = 'https://core.trac.wordpress.org/timeline';
const DAY = 86400000;

const decode = ( s ) => s.replace( /&lt;/g, '<' ).replace( /&gt;/g, '>' ).replace( /&quot;/g, '"' ).replace( /&#39;/g, "'" ).replace( /&amp;/g, '&' );
const tag = ( item, name ) => decode( item.match( new RegExp( `<${ name }>([\\s\\S]*?)</${ name }>` ) )?.[ 1 ] ?? '' ).trim();
const isoDay = ( d ) => d.toISOString().slice( 0, 10 );
const tracDay = ( d ) => `${ String( d.getUTCMonth() + 1 ).padStart( 2, '0' ) }/${ String( d.getUTCDate() ).padStart( 2, '0' ) }/${ String( d.getUTCFullYear() ).slice( 2 ) }`;

const fieldsOf = ( description ) => [ ...description.matchAll( /<i>([^<]+)<\/i>/g ) ].map( ( m ) => m[ 1 ].toLowerCase() );

export function parseTimeline( xml ) {
	return [ ...xml.matchAll( /<item>([\s\S]*?)<\/item>/g ) ].flatMap( ( [ , item ] ) => {
		const rawTitle = tag( item, 'title' );
		const link = tag( item, 'link' );
		const description = tag( item, 'description' );
		const pubDate = tag( item, 'pubDate' );
		const date = pubDate ? isoDay( new Date( pubDate ) ) : '';
		const cs = rawTitle.match( /^Changeset \[(\d+)\]:\s*(.*)$/ );
		if ( cs ) return { ticket: null, changeset: +cs[ 1 ], kind: 'changeset', fields: [], title: cs[ 2 ], link, date };
		// One commit or bulk edit touching several tickets: "Tickets #1,<ZWSP>2 batch updated".
		const batch = rawTitle.match( /^Tickets ([#\d,\u200b\s]+) batch updated$/ );
		if ( batch ) {
			const resolution = description.match( /^(\w+):/ )?.[ 1 ];
			return batch[ 1 ].match( /\d+/g ).map( ( n ) => ( {
				ticket: +n, changeset: null, kind: resolution ? 'closed' : 'updated', ...( resolution && { resolution } ),
				fields: fieldsOf( description ), title: '', link: `https://core.trac.wordpress.org/ticket/${ n }`, date,
			} ) );
		}
		const t = rawTitle.match( /^Tickets? #(\d+) \((.*)\) (created|closed|reopened|updated)$/ );
		if ( ! t ) return { ticket: null, changeset: null, kind: 'updated', fields: [], title: rawTitle, link, date };
		const event = { ticket: +t[ 1 ], changeset: null, kind: t[ 3 ], fields: [], title: t[ 2 ], link, date };
		if ( event.kind === 'closed' ) event.resolution = description.match( /^(\w+):/ )?.[ 1 ];
		event.fields = fieldsOf( description );
		return event;
	} );
}

// Trac treats daysback below 1 as 1, so one request covers the "from" day and the day before.
// Step two days at a time, then keep only the requested days.
export async function fetchTimeline( from, days, fetchFn = fetch ) {
	const start = Date.UTC( from.getUTCFullYear(), from.getUTCMonth(), from.getUTCDate() );
	const wanted = new Set( Array.from( { length: days }, ( _, i ) => isoDay( new Date( start + i * DAY ) ) ) );
	const seen = new Set();
	const events = [];
	for ( let i = 1; i < days + 1; i += 2 ) {
		const url = `${ TIMELINE }?format=rss&ticket=on&ticket_details=on&changeset=on&from=${ tracDay( new Date( start + i * DAY ) ) }&daysback=1&max=5000`;
		const res = await fetchFn( url );
		if ( ! res.ok ) throw new Error( `Trac timeline returned ${ res.status } for ${ url }` );
		for ( const e of parseTimeline( await res.text() ) ) {
			const id = `${ e.link }|${ e.date }|${ e.kind }`;
			if ( wanted.has( e.date ) && ! seen.has( id ) ) {
				seen.add( id );
				events.push( e );
			}
		}
	}
	return events;
}

function parseCsv( text ) {
	const rows = [];
	let row = [], field = '', quoted = false;
	for ( let i = 0; i < text.length; i++ ) {
		const c = text[ i ];
		if ( quoted ) {
			if ( c === '"' && text[ i + 1 ] === '"' ) { field += '"'; i++; }
			else if ( c === '"' ) quoted = false;
			else field += c;
		} else if ( c === '"' ) quoted = true;
		else if ( c === ',' ) { row.push( field ); field = ''; }
		else if ( c === '\n' || c === '\r' ) {
			if ( c === '\r' && text[ i + 1 ] === '\n' ) i++;
			row.push( field ); rows.push( row ); row = []; field = '';
		} else field += c;
	}
	if ( field || row.length ) { row.push( field ); rows.push( row ); }
	return rows.filter( ( r ) => r.some( ( f ) => f !== '' ) );
}

export function parseQueryCsv( text ) {
	const [ head, ...rows ] = parseCsv( text.replace( /^﻿/, '' ) );
	return rows.map( ( values ) => {
		const r = Object.fromEntries( head.map( ( h, i ) => [ h.trim(), values[ i ] ?? '' ] ) );
		return { id: +r.id, summary: r.summary ?? '', status: r.status ?? '', milestone: r.milestone ?? '', keywords: r.keywords ?? '' };
	} );
}
