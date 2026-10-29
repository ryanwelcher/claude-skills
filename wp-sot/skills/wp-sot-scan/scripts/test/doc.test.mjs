import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseDoc, struckKeys } from '../lib/doc.mjs';

const fixture = readFileSync( new URL( 'fixtures/doc-72.md', import.meta.url ), 'utf8' );
const doc = parseDoc( fixture );

test( 'lists every tab from the H1 headings', () => {
	assert.deepEqual( doc.tabs, [ 'WordPress 7.2 Source of Truth: Draft', 'WordPress 7.2 Source of Truth', 'Notes', 'Punted from 7.2', 'Backlog from 7.1' ] );
} );

test( 'finds both scan blocks and their dates', () => {
	assert.equal( doc.blocks.length, 2 );
	assert.equal( doc.blocks[ 0 ].date, 'October 22, 2026' );
	assert.equal( doc.blocks[ 1 ].date, 'October 29, 2026' );
} );

test( 'human text keeps notes written below a footer and drops block contents', () => {
	assert.ok( doc.humanText.includes( 'gutenberg/pull/81888' ) );
	for ( const n of [ '81500', '81777', '81999' ] ) assert.ok( ! doc.humanText.includes( n ), n );
} );

test( 'a block with no footer ends at the next H1', () => {
	assert.ok( doc.blocks[ 1 ].text.includes( '81999' ) );
	assert.ok( ! doc.blocks[ 1 ].text.includes( 'Punted from 7.2' ) );
	assert.ok( doc.humanText.includes( 'Punted from 7.2' ) );
} );

test( 'struck-out candidates are collected by key', () => {
	assert.deepEqual( struckKeys( doc.blocks ), new Set( [ 'WordPress/gutenberg#81500' ] ) );
} );
