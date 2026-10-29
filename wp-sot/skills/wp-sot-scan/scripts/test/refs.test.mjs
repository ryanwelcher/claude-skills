import { test } from 'node:test';
import assert from 'node:assert/strict';
import { refKey, extractRefs } from '../lib/refs.mjs';

test( 'GitHub PRs and issues share one key', () => {
	assert.equal( refKey( 'https://github.com/WordPress/gutenberg/pull/81234' ), 'WordPress/gutenberg#81234' );
	assert.equal( refKey( 'https://github.com/WordPress/gutenberg/issues/81234' ), 'WordPress/gutenberg#81234' );
} );

test( 'Trac tickets key by number, ignoring the comment anchor', () => {
	assert.equal( refKey( 'https://core.trac.wordpress.org/ticket/66187#comment:28' ), 'trac#66187' );
} );

test( 'Make Core posts key by URL without anchor, query or trailing slash', () => {
	const key = 'url:https://make.wordpress.org/core/2026/10/20/some-dev-note';
	assert.equal( refKey( 'https://make.wordpress.org/core/2026/10/20/some-dev-note/' ), key );
	assert.equal( refKey( 'https://make.wordpress.org/core/2026/10/20/some-dev-note/#heading' ), key );
	assert.equal( refKey( 'https://make.wordpress.org/core/2026/10/20/some-dev-note/?x=1' ), key );
} );

test( 'non-URLs have no key', () => {
	assert.equal( refKey( 'not a url' ), null );
} );

test( 'the same link twice gives one ref', () => {
	const refs = extractRefs( 'See https://github.com/WordPress/gutenberg/pull/1 and (https://github.com/WordPress/gutenberg/pull/1).' );
	assert.equal( refs.length, 1 );
	assert.deepEqual( refs[ 0 ], { key: 'WordPress/gutenberg#1', kind: 'github', repo: 'WordPress/gutenberg', number: 1, url: 'https://github.com/WordPress/gutenberg/pull/1' } );
} );
