#!/usr/bin/env node
// After Pass 2: merges Claude's candidates with Pass 1 findings and the candidates still open from
// earlier weeks, writes the scan to the repo, saves state for next week, copies the block to the
// clipboard and prints it.
//
//   node finish.mjs --release-dir <dir> --work <work.json> --candidates <candidates.json> [--no-clipboard]

import { readFileSync, writeFileSync, mkdirSync, mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { refKey } from './lib/refs.mjs';
import { renderBlock } from './lib/block.mjs';

// macOS: put the block on the clipboard as HTML (what Chrome pastes into Google Docs, with the
// heading and links intact) plus plain text as a fallback.
const JXA = `ObjC.import('AppKit');
function run( argv ) {
	const read = ( p ) => $.NSString.stringWithContentsOfFileEncodingError( p, $.NSUTF8StringEncoding, null );
	const pb = $.NSPasteboard.generalPasteboard;
	pb.clearContents;
	pb.setStringForType( read( argv[ 0 ] ), 'public.html' );
	pb.setStringForType( read( argv[ 1 ] ), 'public.utf8-plain-text' );
}`;

export async function copyToClipboard( html, text ) {
	const dir = mkdtempSync( join( tmpdir(), 'sot-scan-' ) );
	writeFileSync( join( dir, 'block.html' ), `<meta charset="utf-8">${ html }` );
	writeFileSync( join( dir, 'block.txt' ), text );
	try {
		execFileSync( 'osascript', [ '-l', 'JavaScript', '-e', JXA, join( dir, 'block.html' ), join( dir, 'block.txt' ) ], { stdio: [ 'ignore', 'ignore', 'pipe' ] } );
		return true;
	} catch ( e ) {
		console.error( `Couldn't copy the block to the clipboard (${ String( e.message || e ).split( '\n' )[ 0 ] }). Copy it from below instead.` );
		return false;
	}
}

const keyOf = ( item ) => item.key ?? refKey( item.url ) ?? `url:${ item.url }`;

export async function finish( opts, deps = { copy: copyToClipboard } ) {
	const work = JSON.parse( readFileSync( opts.work, 'utf8' ) );
	const cands = JSON.parse( readFileSync( opts.candidates, 'utf8' ) );
	const skip = new Set( [ ...work.docKeys, ...work.struckKeys, ...work.findings.map( keyOf ) ] );

	const extra = [];
	for ( const item of [ ...( cands.items ?? [] ), ...work.openCandidates ] ) {
		if ( ! /^https?:\/\//.test( item.url ?? '' ) ) {
			console.error( `Skipped "${ item.text }": every finding needs a full http(s) link.` );
			continue;
		}
		const key = keyOf( item );
		if ( skip.has( key ) ) continue;
		skip.add( key );
		extra.push( { group: item.group ?? 'candidates', text: item.text, url: item.url, key } );
	}
	const findings = [ ...work.findings, ...extra ];

	const notes = [ ...( work.notes ?? [] ) ];
	if ( work.firstRun ) notes.push( 'First scan for this release, so changes to linked items start next week.' );
	if ( ! work.tracCsv ) notes.push( "Trac milestone values weren't checked this week." );
	const checked = [ `${ work.checked.linked } linked tickets and PRs`, cands.checked ].filter( Boolean ).join( ', ' );
	const { markdown, html } = renderBlock( { date: work.date, checked, notes, findings } );

	const notesDir = join( opts.releaseDir, 'notes' );
	mkdirSync( join( notesDir, 'scans' ), { recursive: true } );
	const file = join( notesDir, 'scans', `${ work.date }.md` );
	writeFileSync( file, `---\ntab: ${ work.tab }\n---\n\n${ markdown }` );
	const state = { lastRun: work.date, refs: work.snapshots, openCandidates: extra.filter( ( f ) => f.group === 'candidates' ) };
	writeFileSync( join( notesDir, 'scan-state.json' ), JSON.stringify( state, null, '\t' ) + '\n' );

	await deps.copy( html, markdown );
	return { markdown, file };
}

if ( import.meta.url === pathToFileURL( process.argv[ 1 ] ).href ) {
	const argv = process.argv.slice( 2 );
	const get = ( name ) => argv[ argv.indexOf( `--${ name }` ) + 1 ];
	if ( ! argv.includes( '--release-dir' ) || ! argv.includes( '--work' ) || ! argv.includes( '--candidates' ) ) {
		console.error( 'usage: finish.mjs --release-dir <dir> --work <work.json> --candidates <candidates.json> [--no-clipboard]' );
		process.exit( 2 );
	}
	const copy = argv.includes( '--no-clipboard' ) ? async () => false : copyToClipboard;
	const { markdown, file } = await finish( { releaseDir: get( 'release-dir' ), work: get( 'work' ), candidates: get( 'candidates' ) }, { copy } );
	console.log( markdown );
	console.error( `Saved to ${ file }` );
}
