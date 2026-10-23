#!/usr/bin/env node
// Splits a Google Docs Markdown export of a Source of Truth draft into the content repo layout.
//
//   node import-gdoc.mjs <export.md> <repo-dir>
//
// The repo dir should already hold the repo template. Existing content/post and notes files
// are overwritten. Prints a summary of what went where so the import can be checked by eye.

import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const [ , , input, repo ] = process.argv;
if ( ! input || ! repo ) {
	console.error( 'usage: import-gdoc.mjs <export.md> <repo-dir>' );
	process.exit( 2 );
}

const FLAGS = { '✏': 'edit', '🙏': 'blessed', '🔍': 'check', '🎨': 'visuals', '🏈': 'punted' };
const FLAG_RE = /\s*(✏|🙏|🔍|🎨|🏈)️?/gu;

// Google's export escapes most punctuation. \* stays escaped so literal asterisks survive.
const src = readFileSync( input, 'utf8' )
	.replace( /\\([!#<>\-=|\[\]()+.`~{}_&:'"])/g, '$1' )
	.replace( /[ \t]+$/gm, '' );

const slugify = ( s ) => s.toLowerCase().replace( /<[^>]+>|[`*]/g, '' ).replace( /[^a-z0-9]+/g, '-' ).replace( /^-|-$/g, '' ).slice( 0, 60 );
const pad = ( n, w ) => String( n ).padStart( w, '0' );
const yamlList = ( a ) => `[${ a.join( ', ' ) }]`;
const write = ( rel, text ) => {
	const p = join( repo, rel );
	mkdirSync( join( p, '..' ), { recursive: true } );
	writeFileSync( p, text.replace( /\n{3,}/g, '\n\n' ).trim() + '\n' );
};

function splitFlags( heading ) {
	const flags = [ ...heading.matchAll( FLAG_RE ) ].map( ( m ) => FLAGS[ m[ 1 ] ] );
	return { text: heading.replace( FLAG_RE, '' ).replace( /\*\*/g, '' ).trim(), flags: [ ...new Set( flags ) ] };
}

function takeTags( lines ) {
	const i = lines.findIndex( ( l ) => /^==(\[[^\]]+\]\s*)+==$/.test( l.trim() ) );
	if ( i === -1 ) return { tags: [], lines };
	const tags = [ ...lines[ i ].matchAll( /\[([^\]]+)\]/g ) ].map( ( m ) => m[ 1 ] );
	return { tags, lines: lines.filter( ( _, j ) => j !== i ) };
}

// Split on H1s: the draft header, the post, then Notes / Punted / Backlog.
const lines = src.split( '\n' );
const h1s = lines.map( ( l, i ) => ( /^# /.test( l ) ? i : -1 ) ).filter( ( i ) => i !== -1 );
const block = ( start ) => lines.slice( start + 1, h1s.find( ( i ) => i > start ) ?? lines.length );
const postStart = h1s.find( ( i ) => ! /draft/i.test( lines[ i ] ) && ! /\*\*/.test( lines[ i ] ) );
if ( postStart === undefined ) throw new Error( 'No post H1 (e.g. "# WordPress 7.2 Source of Truth") found' );
const post = block( postStart );
const postText = post.join( '\n' );

const version = lines[ postStart ].match( /(\d+\.\d+)/ )?.[ 1 ] ?? 'X.Y';
const sot = existsSync( join( repo, 'sot.json' ) ) ? JSON.parse( readFileSync( join( repo, 'sot.json' ), 'utf8' ) ) : {};
sot.version = version;
sot.releaseDate = postText.match( /scheduled for release on ([^.]+?)\./i )?.[ 1 ] ?? sot.releaseDate;
sot.gutenbergRange = postText.match( /Gutenberg plugin versions ([\d.]+\s*[–-]\s*[\d.]+)/ )?.[ 1 ] ?? sot.gutenbergRange;
// Milestones come from the notes' schedule table, e.g. "| Beta 1 | October 20, 15:00 UTC |".
const year = sot.releaseDate?.match( /\d{4}/ )?.[ 0 ];
const milestone = ( label ) => {
	const m = src.match( new RegExp( `^\\|\\s*${ label }\\b[^|]*\\|\\s*([A-Z][a-z]+ \\d{1,2})\\b`, 'm' ) );
	const d = m && year ? new Date( `${ m[ 1 ] }, ${ year } 12:00 UTC` ) : null;
	return d && ! isNaN( d ) ? d.toISOString().slice( 0, 10 ) : undefined;
};
sot.milestones = {
	...sot.milestones,
	beta1: milestone( 'Beta 1' ) ?? sot.milestones?.beta1,
	rc1: milestone( 'RC 1' ) ?? sot.milestones?.rc1,
	final: milestone( 'Final' ) ?? sot.milestones?.final,
};
write( 'sot.json', JSON.stringify( sot, null, '\t' ) );

// Template files the import doesn't overwrite still name the release as X.Y.
for ( const rel of [ 'README.md', 'CLAUDE.md', 'notes/punted.md' ] ) {
	const p = join( repo, rel );
	if ( existsSync( p ) ) writeFileSync( p, readFileSync( p, 'utf8' ).replace( /X\.Y/g, version ).replace( /X-Y/g, version.replace( '.', '-' ) ) );
}

// Sections start at the first H2 whose block contains a ==[tag]== line.
const h2s = post.map( ( l, i ) => ( /^## /.test( l ) ? i : -1 ) ).filter( ( i ) => i !== -1 );
const h2End = ( i ) => h2s.find( ( j ) => j > i ) ?? post.length;
const firstSection = h2s.find( ( i ) => post.slice( i, h2End( i ) ).some( ( l ) => /^==\[/.test( l.trim() ) ) ) ?? post.length;

rmSync( join( repo, 'content', 'post' ), { recursive: true, force: true } );
write( 'content/post/00-intro.md', post.slice( 0, firstSection ).join( '\n' ) );

const summary = [];
let sectionNo = 0;
for ( const start of h2s.filter( ( i ) => i >= firstSection ) ) {
	let body = post.slice( start + 1, h2End( start ) );
	// A closing --- in the last section starts the outro.
	const hr = body.findLastIndex( ( l ) => l.trim() === '---' );
	if ( h2End( start ) === post.length && hr !== -1 && ! body.slice( hr ).some( ( l ) => /^### /.test( l ) ) ) {
		write( 'content/post/99-outro.md', body.slice( hr + 1 ).join( '\n' ) );
		body = body.slice( 0, hr );
	}
	const { text: title, flags } = splitFlags( post[ start ].slice( 3 ) );
	const dir = `content/post/${ pad( ( ++sectionNo ) * 10, 2 ) }-${ slugify( title ) }`;
	const h3s = body.map( ( l, i ) => ( /^### /.test( l ) ? i : -1 ) ).filter( ( i ) => i !== -1 );
	const pre = takeTags( body.slice( 0, h3s[ 0 ] ?? body.length ) );
	const fm = [ `title: ${ title }`, pre.tags.length && `tags: ${ yamlList( pre.tags ) }`, flags.length && `flags: ${ yamlList( flags ) }` ].filter( Boolean );
	write( `${ dir }/_section.md`, `---\n${ fm.join( '\n' ) }\n---\n\n${ pre.lines.join( '\n' ) }` );
	summary.push( `${ dir }/ (${ h3s.length } items)` );

	h3s.forEach( ( h, n ) => {
		const item = splitFlags( body[ h ].slice( 4 ) );
		const { tags, lines: rest } = takeTags( body.slice( h + 1, h3s[ n + 1 ] ?? body.length ) );
		const meta = [ `title: ${ item.text }`, `tags: ${ yamlList( tags ) }`, item.flags.length && `flags: ${ yamlList( item.flags ) }` ].filter( Boolean );
		const file = `${ dir }/${ pad( ( n + 1 ) * 10, 3 ) }-${ slugify( item.text ) }.md`;
		write( file, `---\n${ meta.join( '\n' ) }\n---\n\n${ rest.join( '\n' ) }` );
		summary.push( `  ${ file.split( '/' ).pop() }${ tags.length ? '' : '  (no tags)' }` );
	} );
}

// Notes and the trailing H1 blocks.
const notesH1 = h1s.find( ( i ) => /^# \*\*Notes\*\*/.test( lines[ i ] ) );
if ( notesH1 !== undefined ) {
	const notes = block( notesH1 );
	const nh2 = notes.map( ( l, i ) => ( /^## /.test( l ) ? i : -1 ) ).filter( ( i ) => i !== -1 );
	const research = [ notes.slice( 0, nh2[ 0 ] ?? notes.length ) ];
	const sweeps = [];
	const questions = [];
	nh2.forEach( ( s, n ) => {
		const chunk = notes.slice( s, nh2[ n + 1 ] ?? notes.length );
		if ( /^## \**Sweep/i.test( notes[ s ] ) ) sweeps.push( chunk );
		else if ( /^## \**Open questions/i.test( notes[ s ] ) ) questions.push( chunk.slice( 1 ) );
		else research.push( chunk );
	} );
	write( 'notes/research.md', `# Notes\n\n${ research.map( ( c ) => c.join( '\n' ) ).join( '\n' ) }` );
	write( 'notes/sweep-log.md', `# Sweep log\n\nNewest first.\n\n${ sweeps.map( ( c ) => c.join( '\n' ).replace( /^## /, '## ' ) ).join( '\n\n' ) }` );
	write( 'notes/open-questions.md', `# Open questions\n\n${ questions.map( ( c ) => c.join( '\n' ) ).join( '\n' ) }` );
	summary.push( `notes/research.md, notes/sweep-log.md (${ sweeps.length } sweeps), notes/open-questions.md` );
}
for ( const i of h1s.filter( ( i ) => i > postStart && i !== notesH1 ) ) {
	const name = lines[ i ].replace( /[#*]/g, '' ).trim();
	const file = /punt/i.test( name ) ? 'notes/punted.md' : /backlog/i.test( name ) ? 'notes/backlog.md' : `notes/${ slugify( name ) }.md`;
	write( file, `# ${ name }\n\n${ block( i ).join( '\n' ) }` );
	summary.push( file );
}

console.log( `Imported WordPress ${ version } (release ${ sot.releaseDate ?? '?' }, Gutenberg ${ sot.gutenbergRange ?? '?' })` );
console.log( summary.join( '\n' ) );
