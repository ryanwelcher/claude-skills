#!/usr/bin/env node
// Pass 1 of a scan: reads the Doc export, checks everything people linked in it, and writes a
// work file for Claude's Pass 2 research and for finish.mjs.
//
//   node prepare.mjs --release-dir <dir> --doc <export.md> [--tab Notes] [--date YYYY-MM-DD]
//                    [--trac-linked <csv>] [--trac-milestone <csv>] --out <work.json>
//   node prepare.mjs --doc <export.md> --list-trac     linked Trac ticket numbers, comma-separated

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { basename, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseDoc, struckKeys, unescapeExport } from './lib/doc.mjs';
import { extractRefs } from './lib/refs.mjs';
import { fetchTimeline, parseQueryCsv } from './lib/trac.mjs';
import { lookupGithub, lookupDevnote, tracViaGithub, pool } from './lib/lookup.mjs';
import { diffRefs, tracFindings } from './lib/diff.mjs';

const DAY = 86400000;
const MAX_DAYS = 31;

function readDoc( path ) {
	const text = readFileSync( path, 'utf8' );
	const head = text.slice( 0, 2048 );
	if ( /<html/i.test( head ) || head.includes( 'accounts.google.com' ) ) {
		throw new Error( 'The Doc export is a Google sign-in page. Check the Doc is shared as "anyone with the link", or download it with File > Download > Markdown.' );
	}
	return parseDoc( text );
}

const linkedRefs = ( doc ) => extractRefs( unescapeExport( doc.humanText ) );

export async function prepare( opts, deps = { lookupGithub, lookupDevnote, fetchTimeline, tracViaGithub } ) {
	const tab = opts.tab ?? 'Notes';
	const date = opts.date ?? new Date().toISOString().slice( 0, 10 );
	const doc = readDoc( opts.doc );
	const wanted = tab.toLowerCase();
	if ( ! doc.tabs.some( ( t ) => t.toLowerCase() === wanted || t.toLowerCase().includes( wanted ) ) ) {
		throw new Error( `There's no "${ tab }" tab in the Doc. Tabs found: ${ doc.tabs.join( ', ' ) }.` );
	}

	const statePath = join( opts.releaseDir, 'notes', 'scan-state.json' );
	const state = existsSync( statePath ) ? JSON.parse( readFileSync( statePath, 'utf8' ) ) : null;
	const version = basename( opts.releaseDir );
	const refs = linkedRefs( doc );

	const snapshots = {};
	await pool( refs.filter( ( r ) => r.kind === 'github' || r.kind === 'devnote' ), 4, async ( ref ) => {
		snapshots[ ref.key ] = ref.kind === 'github' ? await deps.lookupGithub( ref ) : await deps.lookupDevnote( ref );
	} );

	// Trac: the timeline since the last run (or the last week), GitHub's mirror of Core commits,
	// and the query CSVs when Chrome fetched them.
	const end = Date.parse( `${ date }T00:00:00Z` );
	let start = state?.lastRun ? Date.parse( `${ state.lastRun }T00:00:00Z` ) : end - 7 * DAY;
	start = Math.max( start, end - MAX_DAYS * DAY );
	const notes = [];
	let events = [];
	try {
		events = await deps.fetchTimeline( new Date( start ), Math.round( ( end - start ) / DAY ) );
	} catch {
		notes.push( "The Trac timeline wasn't reachable this week." );
	}
	const linked = new Set( refs.filter( ( r ) => r.kind === 'trac' ).map( ( r ) => r.key ) );
	const ghTrac = {};
	for ( const key of linked ) {
		try {
			ghTrac[ key.slice( 5 ) ] = await deps.tracViaGithub( +key.slice( 5 ) );
		} catch {
			// Leave the ticket to the timeline and CSV.
		}
	}
	const rows = new Map();
	for ( const file of [ opts.tracLinked, opts.tracMilestone ].filter( Boolean ) ) {
		for ( const row of parseQueryCsv( readFileSync( file, 'utf8' ) ) ) rows.set( row.id, row );
	}
	const tracCsv = Boolean( opts.tracLinked && opts.tracMilestone );
	const trac = tracFindings( { linked, events, csvRows: rows.size ? [ ...rows.values() ] : null, prev: state?.refs ?? null, milestone: version, ghTrac } );
	Object.assign( snapshots, trac.snapshots );

	// A lookup that failed this week keeps last week's snapshot, and refs nobody looked at this week
	// (unlinked milestone tickets when there's no CSV) carry forward, so the baseline never resets.
	const prevRefs = state?.refs ?? {};
	for ( const [ key, snap ] of Object.entries( snapshots ) ) {
		if ( ( snap.error || snap.state === 'unknown' ) && prevRefs[ key ] ) snapshots[ key ] = prevRefs[ key ];
	}
	const merged = { ...prevRefs, ...snapshots };

	return {
		date,
		version,
		tab,
		firstRun: ! state,
		tracCsv,
		docKeys: refs.map( ( r ) => r.key ),
		struckKeys: [ ...struckKeys( doc.blocks ) ],
		findings: [ ...diffRefs( state?.refs ?? null, snapshots, refs ), ...trac.findings ],
		snapshots: merged,
		notes,
		newTickets: trac.newTickets,
		openCandidates: state?.openCandidates ?? [],
		checked: { linked: refs.filter( ( r ) => r.kind !== 'link' ).length },
	};
}

function args( argv ) {
	const out = {};
	for ( let i = 0; i < argv.length; i++ ) {
		const name = argv[ i ].replace( /^--/, '' ).replace( /-(\w)/g, ( _, c ) => c.toUpperCase() );
		out[ name ] = argv[ i + 1 ] && ! argv[ i + 1 ].startsWith( '--' ) ? argv[ ++i ] : true;
	}
	return out;
}

if ( import.meta.url === pathToFileURL( process.argv[ 1 ] ).href ) {
	const opts = args( process.argv.slice( 2 ) );
	try {
		if ( opts.listTrac ) {
			console.log( linkedRefs( readDoc( opts.doc ) ).filter( ( r ) => r.kind === 'trac' ).map( ( r ) => r.number ).join( ',' ) );
		} else {
			if ( ! opts.releaseDir || ! opts.doc || ! opts.out ) throw new Error( 'usage: prepare.mjs --release-dir <dir> --doc <export.md> --out <work.json> [--tab Notes] [--date YYYY-MM-DD] [--trac-linked <csv>] [--trac-milestone <csv>]' );
			const work = await prepare( opts );
			writeFileSync( opts.out, JSON.stringify( work, null, '\t' ) + '\n' );
			console.log( `${ work.findings.length } changes, ${ work.newTickets.length } new milestone tickets, ${ work.openCandidates.length } open candidates. Work file: ${ opts.out }` );
		}
	} catch ( e ) {
		console.error( e.message );
		process.exit( 2 );
	}
}
