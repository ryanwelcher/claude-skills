// Link extraction for the scan. A ref's key is its identity everywhere: in the Doc, in scan
// blocks, in candidates and in scan-state.json.

const URL_RE = /https?:\/\/[^\s)\]>"'`]+/g;

export function refKey( url ) {
	let m = url.match( /^https?:\/\/github\.com\/([\w.-]+\/[\w.-]+)\/(?:pull|issues)\/(\d+)/ );
	if ( m ) return `${ m[ 1 ] }#${ m[ 2 ] }`;
	m = url.match( /^https?:\/\/core\.trac\.wordpress\.org\/ticket\/(\d+)/ );
	if ( m ) return `trac#${ m[ 1 ] }`;
	m = url.match( /^(https?:\/\/make\.wordpress\.org\/core\/[^?#]*)/ );
	if ( m ) return `url:${ m[ 1 ] }`;
	return null;
}

function toRef( url ) {
	const key = refKey( url );
	if ( ! key ) return null;
	if ( key.startsWith( 'trac#' ) ) return { key, kind: 'trac', number: +key.slice( 5 ), url: `https://core.trac.wordpress.org/ticket/${ key.slice( 5 ) }` };
	if ( key.startsWith( 'url:' ) ) return { key, kind: 'devnote', url: key.slice( 4 ) };
	const [ repo, number ] = key.split( '#' );
	return { key, kind: 'github', repo, number: +number, url: url.replace( /[?#].*$/, '' ) };
}

export function extractRefs( text ) {
	const refs = new Map();
	for ( const [ raw ] of text.matchAll( URL_RE ) ) {
		const ref = toRef( raw.replace( /[.,;:]+$/, '' ) );
		if ( ref && ! refs.has( ref.key ) ) refs.set( ref.key, ref );
	}
	return [ ...refs.values() ];
}
