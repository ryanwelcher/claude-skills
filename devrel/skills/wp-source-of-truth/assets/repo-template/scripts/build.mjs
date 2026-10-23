#!/usr/bin/env node
// Builds the Source of Truth from content/post/ into two pages:
//   dist/index.html        the clean post readers see. Working markers (✏️ 🙏 🔍 🎨 🏈),
//                          <!-- --> notes and unpublished items never reach it.
//   dist/draft/index.html  the review copy: notes shown as callouts, flags as badges, hidden
//                          items included and labelled, open questions at the end, noindex.

import { readFileSync, readdirSync, statSync, mkdirSync, writeFileSync, existsSync, cpSync } from 'node:fs';
import { join } from 'node:path';
import { marked } from 'marked';

const ROOT = new URL( '..', import.meta.url ).pathname;
const POST = join( ROOT, 'content', 'post' );
const OUT = join( ROOT, 'dist' );
const release = JSON.parse( readFileSync( join( ROOT, 'sot.json' ), 'utf8' ) );

const MARKERS = /\s*(?:✏|🙏|🔍|🎨|🏈)️?/gu;
const HAS_MARKER = /(?:✏|🙏|🔍|🎨|🏈)/u;
const FLAG_EMOJI = { edit: '✏️', blessed: '🙏', check: '🔍', visuals: '🎨', punted: '🏈' };

function parseFrontmatter( src ) {
	const m = src.match( /^---\n([\s\S]*?)\n---\n?/ );
	if ( ! m ) return { data: {}, body: src };
	const data = {};
	for ( const line of m[ 1 ].split( '\n' ) ) {
		const kv = line.match( /^(\w+):\s*(.*)$/ );
		if ( ! kv ) continue;
		let [ , key, value ] = kv;
		value = value.trim();
		if ( value.startsWith( '[' ) ) {
			value = value.slice( 1, -1 ).split( ',' ).map( ( v ) => v.trim().replace( /^["']|["']$/g, '' ) ).filter( Boolean );
		} else if ( value === 'true' || value === 'false' ) {
			value = value === 'true';
		} else {
			value = value.replace( /^["']|["']$/g, '' );
		}
		data[ key ] = value;
	}
	return { data, body: src.slice( m[ 0 ].length ) };
}

function slugify( s ) {
	return s.toLowerCase().replace( /<[^>]+>|`/g, '' ).replace( /[^a-z0-9]+/g, '-' ).replace( /^-|-$/g, '' );
}

const escapeHtml = ( s ) => s.replace( /&/g, '&amp;' ).replace( /</g, '&lt;' ).replace( />/g, '&gt;' );

function tagChips( tags ) {
	if ( ! tags?.length ) return '';
	return `<p class="tags">${ tags.map( ( t ) => `<span class="tag" data-tag="${ slugify( t ) }">[${ t }]</span>` ).join( ' ' ) }</p>\n`;
}

function byName( dir ) {
	return readdirSync( dir ).filter( ( f ) => ! f.startsWith( '.' ) ).sort();
}

function render( draft ) {
	const toc = [];
	const parts = [];
	const allTags = new Set();
	const usedIds = new Set();
	const warnings = [];

	function uniqueId( base ) {
		let id = base || 'section';
		for ( let n = 2; usedIds.has( id ); n++ ) id = `${ base }-${ n }`;
		usedIds.add( id );
		return id;
	}

	// Gives h2–h4 headings ids and records them for the table of contents.
	function anchorHeadings( html, levels, prefix = '' ) {
		return html.replace( /<h([2-4])>(.*?)<\/h\1>/g, ( match, level, text ) => {
			if ( ! levels.includes( +level ) ) return match;
			const id = uniqueId( prefix + slugify( text ) );
			toc.push( { level: +level, title: text, id } );
			return `<h${ level } id="${ id }">${ text }</h${ level }>`;
		} );
	}

	function prepare( md, where ) {
		let out;
		if ( draft ) {
			out = md.replace( /<!--([\s\S]*?)-->/g, ( _, note ) => `<span class="note">${ escapeHtml( note.trim() ) }</span>` );
		} else {
			out = md.replace( /<!--[\s\S]*?-->/g, '' );
			if ( HAS_MARKER.test( out ) ) warnings.push( `${ where }: working marker in published text (stripped)` );
			out = out.replace( MARKERS, '' );
			if ( /Month Day|TODO|TBD/.test( out ) ) warnings.push( `${ where }: placeholder text still present` );
		}
		// ==[tag] [tag]== lines become tag chips.
		return out.replace( /^==((?:\[[^\]]+\]\s*)+)==\s*$/gm, ( _, tags ) => tagChips( [ ...tags.matchAll( /\[([^\]]+)\]/g ) ].map( ( t ) => t[ 1 ] ) ) );
	}

	for ( const entry of byName( POST ) ) {
		const path = join( POST, entry );
		if ( statSync( path ).isFile() && entry.endsWith( '.md' ) ) {
			const { body } = parseFrontmatter( readFileSync( path, 'utf8' ) );
			parts.push( anchorHeadings( marked.parse( prepare( body, entry ) ), [ 2, 3 ] ) );
			continue;
		}
		if ( ! statSync( path ).isDirectory() ) continue;

		const section = parseFrontmatter( readFileSync( join( path, '_section.md' ), 'utf8' ) );
		const sectionTitle = section.data.title || entry;
		const items = [];
		for ( const file of byName( path ).filter( ( f ) => f.endsWith( '.md' ) && f !== '_section.md' ) ) {
			const where = `${ entry }/${ file }`;
			const { data, body } = parseFrontmatter( readFileSync( join( path, file ), 'utf8' ) );
			if ( data.published === false && ! draft ) continue;
			if ( ! data.title ) {
				warnings.push( `${ where }: missing title, skipped` );
				continue;
			}
			items.push( { where, data, body } );
		}
		// A section whose items are all hidden (e.g. New Blocks after both missed Beta 1) is left out.
		if ( ! items.length ) continue;

		const sectionId = uniqueId( slugify( sectionTitle ) );
		toc.push( { level: 2, title: sectionTitle, id: sectionId } );
		let html = `<section class="sot-section" id="${ sectionId }">\n<h2>${ sectionTitle }</h2>\n`;
		html += tagChips( section.data.tags );
		html += marked.parse( prepare( section.body, `${ entry }/_section.md` ) );

		for ( const { where, data, body } of items ) {
			const tags = Array.isArray( data.tags ) ? data.tags : [];
			// Untagged items (e.g. under Developer Goodies) filter by their section's tags; with
			// none there either, they stay visible under every filter rather than vanishing.
			const filterTags = tags.length ? tags : section.data.tags?.length ? section.data.tags : [ 'all' ];
			filterTags.forEach( ( t ) => allTags.add( t ) );
			const id = uniqueId( data.slug || slugify( data.title ) );
			const title = marked.parseInline( draft ? data.title : prepare( data.title, where ).trim() );
			toc.push( { level: 3, title, id } );
			const hidden = data.published === false;
			const flags = Array.isArray( data.flags ) ? data.flags : [];
			const badges = draft
				? `${ hidden ? '<span class="badge hidden-badge">Hidden on the live post</span>' : '' }${ flags.map( ( f ) => `<span class="badge">${ FLAG_EMOJI[ f ] ?? '' } ${ f }</span>` ).join( '' ) }<span class="badge file">${ where }</span>`
				: '';
			html += `<article class="sot-item${ hidden ? ' unpublished' : '' }" id="${ id }" data-tags="${ filterTags.map( slugify ).join( ' ' ) }">\n`;
			html += `<h3><a class="anchor" href="#${ id }">${ title }</a></h3>\n${ badges ? `<p class="badges">${ badges }</p>\n` : '' }${ tagChips( tags ) }`;
			html += anchorHeadings( marked.parse( prepare( body, where ) ), [ 4 ], `${ id }-` );
			html += '</article>\n';
		}
		parts.push( html + '</section>\n' );
	}

	if ( draft && existsSync( join( ROOT, 'notes', 'open-questions.md' ) ) ) {
		const md = readFileSync( join( ROOT, 'notes', 'open-questions.md' ), 'utf8' ).replace( /^# .*$/m, '## Open questions (draft only)' );
		parts.push( `<section class="sot-section draft-only">${ anchorHeadings( marked.parse( md ), [ 2 ] ) }</section>` );
	}

	return { toc, parts, allTags, warnings };
}

// Numbered, nested table of contents like the published Source of Truth posts.
function tocList( items ) {
	let out = '<ol>';
	for ( let i = 0; i < items.length; i++ ) {
		const t = items[ i ];
		const children = [];
		while ( items[ i + 1 ] && items[ i + 1 ].level > t.level ) children.push( items[ ++i ] );
		out += `<li><a href="#${ t.id }">${ t.title.replace( /<[^>]+>/g, '' ) }</a>${ children.length ? tocList( children ) : '' }</li>`;
	}
	return out + '</ol>';
}

function page( { toc, parts, allTags }, draft ) {
	const filterHtml = [ ...allTags ]
		.filter( ( t ) => t !== 'all' )
		.map( ( t ) => `<button type="button" data-filter="${ slugify( t ) }" aria-pressed="false">${ t }</button>` )
		.join( '' );
	const title = `WordPress ${ release.version } Source of Truth`;
	const updated = new Date().toLocaleDateString( 'en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' } );
	const words = parts.join( ' ' ).replace( /<[^>]+>/g, ' ' ).split( /\s+/ ).filter( Boolean ).length;
	const author = release.author?.name
		? `Written by ${ release.author.url ? `<a href="${ release.author.url }">${ release.author.name }</a>` : release.author.name }${ release.published ? ` · ${ release.published }` : '' } · `
		: '';
	const byline = `${ author }Updated ${ updated } · Estimated reading time ${ Math.round( words / 240 ) }–${ Math.round( words / 160 ) } minutes (${ words.toLocaleString( 'en-US' ) } words)`;
	let body = parts.join( '\n' );
	// The draft lives one level down, so asset paths need to climb back up.
	if ( draft ) body = body.replace( /(src|href)="assets\//g, '$1="../assets/' );

	return {
		words,
		html: `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${ draft ? `Draft: ${ title }` : title }</title>
${ draft ? '<meta name="robots" content="noindex, nofollow">' : `<meta name="description" content="Everything coming in WordPress ${ release.version }, tagged by audience, with links to learn more.">` }
<style>
:root{--bg:#fff;--fg:#1e1e1e;--muted:#5a5a5a;--line:#e0e0e0;--accent:#3858e9;--chip:#eef1fd;--code:#f4f4f4;--note:#fff6d6;--note-line:#e8c547}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141414;--fg:#ececec;--muted:#a8a8a8;--line:#2e2e2e;--accent:#8fa4ff;--chip:#20264a;--code:#222;--note:#3a3214;--note-line:#a68a1f}}
:root[data-theme="dark"]{--bg:#141414;--fg:#ececec;--muted:#a8a8a8;--line:#2e2e2e;--accent:#8fa4ff;--chip:#20264a;--code:#222;--note:#3a3214;--note-line:#a68a1f}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}
.wrap{display:grid;grid-template-columns:260px minmax(0,1fr);gap:48px;max-width:1180px;margin:0 auto;padding:32px 16px}
nav{position:sticky;top:16px;align-self:start;max-height:calc(100vh - 32px);overflow:auto;font-size:14px}
nav ol{padding-left:18px;margin:0}
nav>ol{padding-left:22px}
nav li{margin:2px 0}
nav ol ol{color:var(--muted);font-size:13px}
nav .toc-title{font-weight:600;margin:0 0 8px}
nav a{text-decoration:none;color:inherit}
nav a:hover{color:var(--accent)}
figcaption,img+em{display:block;color:var(--muted);font-size:14px}
main{max-width:760px;min-width:0}
header h1{font-size:2.2rem;line-height:1.2;margin:0 0 4px}
header p{color:var(--muted);margin:0 0 24px}
.filters{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 32px}
.filters button{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:999px;padding:4px 12px;cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--bg)}
h2{margin-top:56px;padding-top:16px;border-top:1px solid var(--line)}
h3 .anchor{color:inherit;text-decoration:none}
.tags{margin:-8px 0 12px}
.tag{display:inline-block;font-size:13px;background:var(--chip);border-radius:4px;padding:0 6px;margin-right:4px}
code{background:var(--code);padding:1px 4px;border-radius:3px;font-size:.9em;overflow-wrap:anywhere}
kbd{border:1px solid var(--line);border-radius:3px;padding:0 4px;font-size:.85em}
table{border-collapse:collapse;display:block;overflow-x:auto}td,th{border:1px solid var(--line);padding:4px 8px}
img,video{max-width:100%;height:auto}
.sot-item.hidden{display:none}
.banner{background:var(--note);border:1px solid var(--note-line);border-radius:6px;padding:8px 12px;margin:0 0 24px;font-size:15px}
.note{display:block;background:var(--note);border-left:3px solid var(--note-line);padding:6px 10px;margin:8px 0;font-size:14px;white-space:pre-wrap}
.badges{margin:-8px 0 8px;display:flex;flex-wrap:wrap;gap:4px}
.badge{font-size:12px;border:1px solid var(--line);border-radius:4px;padding:0 6px;color:var(--muted)}
.badge.file{font-family:ui-monospace,monospace}
.hidden-badge{border-color:var(--note-line);color:var(--fg);background:var(--note)}
.unpublished{opacity:.6}
footer{color:var(--muted);font-size:14px;margin-top:64px}
@media (max-width:860px){.wrap{grid-template-columns:1fr}nav{position:static;max-height:none}}
</style>
</head>
<body>
<div class="wrap">
<nav aria-label="Table of Contents"><p class="toc-title">Table of Contents</p>${ tocList( toc ) }</nav>
<main>
<header><h1>${ title }</h1><p>${ byline }</p></header>
${ draft ? '<p class="banner"><strong>Draft review copy.</strong> Working notes, markers and hidden items are shown. Readers see <a href="../">the clean post</a>.</p>' : '' }
<div class="filters" role="group" aria-label="Filter by audience">${ filterHtml }</div>
${ body }
<footer>${ release.canonicalUrl ? `Also published at <a href="${ release.canonicalUrl }">${ release.canonicalUrl }</a>.` : '' }</footer>
</main>
</div>
<script>
const buttons=[...document.querySelectorAll('.filters button')];
buttons.forEach(b=>b.addEventListener('click',()=>{
	b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');
	const on=buttons.filter(x=>x.getAttribute('aria-pressed')==='true').map(x=>x.dataset.filter);
	document.querySelectorAll('.sot-item').forEach(a=>{
		const tags=a.dataset.tags.split(' ');
		a.classList.toggle('hidden',on.length>0&&!on.some(t=>tags.includes(t)||tags.includes('all')));
	});
}));
</script>
</body>
</html>
`,
	};
}

const clean = render( false );
const draft = render( true );
const live = page( clean, false );
mkdirSync( join( OUT, 'draft' ), { recursive: true } );
// Images and videos referenced as assets/… in the content.
if ( existsSync( join( ROOT, 'content', 'assets' ) ) ) cpSync( join( ROOT, 'content', 'assets' ), join( OUT, 'assets' ), { recursive: true } );
writeFileSync( join( OUT, 'index.html' ), live.html );
writeFileSync( join( OUT, 'draft', 'index.html' ), page( draft, true ).html );
console.log( `Built dist/index.html (${ ( live.html.match( /<article /g ) || [] ).length } items, ${ live.words } words) and dist/draft/index.html` );
for ( const w of clean.warnings ) console.warn( `warning: ${ w }` );
if ( process.argv.includes( '--strict' ) && clean.warnings.length ) process.exit( 1 );
