// Turns this run's lookups, compared with the last run's state, into block findings.

const TICKET = 'https://core.trac.wordpress.org/ticket/';

// Titles come from other people's tickets and PRs; keep em-dashes out of the block.
const clean = ( s ) => ( s ?? '' ).replace( /\s*—\s*/g, ', ' ).trim();
const sentence = ( s ) => ( /[.!?]$/.test( s ) ? s : `${ s }.` );
const ticketLabel = ( n, title ) => clean( `#${ n } ${ clean( title ) }` );
const usable = ( s ) => s && ! s.error && s.state !== 'unknown';

export function diffRefs( prev, curr, refs ) {
	if ( ! prev ) return [];
	const findings = [];
	for ( const ref of refs ) {
		if ( ref.kind === 'trac' ) continue;
		const before = prev[ ref.key ];
		const now = curr[ ref.key ];
		if ( ! usable( before ) || ! usable( now ) || before.state === now.state ) continue;
		const title = clean( now.title || before.title );
		let text = null;
		if ( ref.kind === 'devnote' ) {
			if ( now.state === 'missing' ) text = `Link broken: ${ title }`;
		} else if ( now.state === 'merged' ) text = `Merged: ${ title }`;
		else if ( now.state === 'open' ) text = `Reopened: ${ title }`;
		else if ( now.state === 'closed' ) text = ref.url.includes( '/pull/' ) ? `Closed without merging: ${ title }` : `Closed: ${ title }`;
		if ( text ) findings.push( { group: 'changes', text: sentence( text ), url: ref.url, key: ref.key } );
	}
	return findings;
}

const isClosed = ( state ) => ( state ?? '' ).startsWith( 'closed' );

export function tracFindings( { linked, events, csvRows, prev, milestone, ghTrac = {} } ) {
	const findings = [];
	const snapshots = {};
	const newTickets = [];
	const closedNow = new Set();
	const add = ( n, text, url = `${ TICKET }${ n }` ) => findings.push( { group: 'changes', text: sentence( text ), url, key: `trac#${ n }` } );
	const fromCsv = new Set();

	for ( const row of csvRows ?? [] ) {
		const key = `trac#${ row.id }`;
		const before = prev?.[ key ];
		const state = row.status === 'closed' && row.resolution ? `closed/${ row.resolution }` : row.status;
		snapshots[ key ] = { title: row.summary, state, milestone: row.milestone, keywords: row.keywords };
		fromCsv.add( row.id );
		if ( ! linked.has( key ) ) {
			if ( row.milestone === milestone && ! before ) newTickets.push( { number: row.id, summary: row.summary, url: `${ TICKET }${ row.id }` } );
			continue;
		}
		// No baseline yet (first run, or last week had no CSV): record, don't compare.
		if ( ! before || before.state === 'unknown' ) continue;
		const label = ticketLabel( row.id, row.summary );
		if ( before.milestone && row.milestone !== before.milestone ) add( row.id, `Moved to ${ row.milestone || 'no milestone' }: ${ label }` );
		if ( isClosed( state ) && ! isClosed( before.state ) ) {
			add( row.id, `Closed (${ row.resolution || 'closed' }): ${ label }` );
			closedNow.add( row.id );
		} else if ( ! isClosed( state ) && isClosed( before.state ) ) add( row.id, `Reopened: ${ label }` );
	}

	// Without the CSV, the timeline says what happened but not the new values. The feed is newest
	// first, so the first status event per ticket is the latest one.
	const latest = new Map();
	const milestoneMoved = new Map();
	for ( const e of events ) {
		// With the CSV, its values win, except on the first run, when only the timeline can say
		// what happened this week.
		if ( ! e.ticket || ( prev && fromCsv.has( e.ticket ) ) || ! linked.has( `trac#${ e.ticket }` ) ) continue;
		if ( ( e.kind === 'closed' || e.kind === 'reopened' ) && ! latest.has( e.ticket ) ) latest.set( e.ticket, e );
		if ( e.fields.includes( 'milestone' ) && ! milestoneMoved.has( e.ticket ) ) milestoneMoved.set( e.ticket, e );
	}
	for ( const key of linked ) {
		const n = +key.slice( 5 );
		if ( prev && fromCsv.has( n ) ) continue;
		const before = prev?.[ key ];
		const snap = fromCsv.has( n ) ? { ...snapshots[ key ] } : { title: before?.title ?? '', state: before?.state ?? 'unknown' };
		if ( before?.milestone && ! fromCsv.has( n ) ) snap.milestone = before.milestone;
		const status = latest.get( n );
		const moved = milestoneMoved.get( n );
		const label = ticketLabel( n, status?.title || moved?.title || snap.title );
		if ( status?.kind === 'closed' ) {
			if ( ! fromCsv.has( n ) ) snap.state = `closed/${ status.resolution || 'closed' }`;
			add( n, `Closed (${ status.resolution || 'closed' }): ${ label }` );
			closedNow.add( n );
		} else if ( status?.kind === 'reopened' ) {
			if ( ! fromCsv.has( n ) ) snap.state = 'reopened';
			add( n, `Reopened: ${ label }` );
		}
		if ( moved && fromCsv.has( n ) ) add( n, `Moved to ${ snap.milestone || 'no milestone' }: ${ label }` );
		else if ( moved ) add( n, `Milestone changed on ${ label.replace( /\.$/, '' ) }, check whether it was punted` );
		if ( ! fromCsv.has( n ) && ( status?.title || moved?.title ) ) snap.title = status?.title || moved?.title;
		snapshots[ key ] = snap;
	}

	// GitHub's mirror of Core commits, for every linked ticket.
	for ( const key of linked ) {
		const n = +key.slice( 5 );
		const gh = ghTrac[ n ];
		if ( ! gh ) {
			// Lookup failed: keep last week's count so next week still compares.
			if ( typeof prev?.[ key ]?.commits === 'number' ) snapshots[ key ] = { ...snapshots[ key ], commits: prev[ key ].commits };
			continue;
		}
		snapshots[ key ] = { ...snapshots[ key ], commits: gh.commits.length };
		const before = prev?.[ key ]?.commits;
		if ( prev && typeof before === 'number' && gh.commits.length > before && ! closedNow.has( n ) && gh.commits[ 0 ] ) {
			add( n, `Committed: #${ n } ${ clean( gh.commits[ 0 ].subject ).replace( /\.$/, '' ) }`, gh.commits[ 0 ].url );
		}
	}
	return { findings, snapshots, newTickets };
}
