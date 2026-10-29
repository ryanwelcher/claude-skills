// Reads a Google Docs Markdown export of a Source of Truth Doc: its tabs, the automated scan
// blocks, and the text people wrote (everything outside the blocks).

import { extractRefs } from './refs.mjs';

// Google's export escapes most punctuation. Same rule as wp-source-of-truth's import-gdoc.mjs.
export const unescapeExport = ( md ) => md.replace( /\\([!#<>\-=|\[\]()+.`~{}_&:'"])/g, '$1' );

const plain = ( line ) => unescapeExport( line ).replace( /^#+\s*/, '' ).replace( /\*/g, '' ).trim();
const START_RE = /^Automated scan results: (.+)$/;
const END_RE = /^End of automated scan results: (.+)$/;

export function parseDoc( markdown ) {
	const lines = markdown.split( '\n' );
	const tabs = [];
	const blocks = [];
	const human = [];
	let block = null;

	const close = () => {
		if ( block ) blocks.push( { date: block.date, text: block.lines.join( '\n' ) } );
		block = null;
	};

	for ( const line of lines ) {
		const isH1 = /^# /.test( line );
		const text = plain( line );
		// A heading, or a plain-text paste of one ("\#\# Automated scan results: ...").
		const start = ! isH1 ? text.match( START_RE ) : null;
		if ( isH1 ) {
			close();
			tabs.push( text );
		}
		if ( start ) {
			close();
			block = { date: start[ 1 ], lines: [ line ] };
			continue;
		}
		if ( block ) {
			block.lines.push( line );
			if ( END_RE.test( text ) ) close();
			continue;
		}
		human.push( line );
	}
	close();
	return { tabs, blocks, humanText: human.join( '\n' ) };
}

export function struckKeys( blocks ) {
	const keys = new Set();
	for ( const { text } of blocks ) {
		// Striking any part of a line strikes the whole finding, link included.
		for ( const line of unescapeExport( text ).split( '\n' ) ) {
			if ( ! /~~[\s\S]+?~~/.test( line ) ) continue;
			for ( const ref of extractRefs( line ) ) keys.add( ref.key );
		}
	}
	return keys;
}
