// Renders one scan as the block that gets pasted into the Doc: Markdown for the repo and the
// session, HTML for the clipboard so the heading and links paste as real formatting.

const MONTHS = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ];
const longDate = ( iso ) => {
	const [ y, m, d ] = iso.split( '-' ).map( Number );
	return `${ MONTHS[ m - 1 ] } ${ d }, ${ y }`;
};
const noDash = ( s ) => s.replace( /\s*—\s*/g, ', ' );
const esc = ( s ) => s.replace( /&/g, '&amp;' ).replace( /</g, '&lt;' ).replace( />/g, '&gt;' ).replace( /"/g, '&quot;' );
const sentence = ( s ) => ( /[.!?]$/.test( s ) ? s : `${ s }.` );

const GROUPS = [
	{ id: 'changes', heading: 'Changes to linked items', empty: 'No changes to linked items' },
	{ id: 'candidates', heading: 'New candidates (not in the Doc yet)', empty: 'No new candidates' },
];

export function renderBlock( { date, checked, notes, findings } ) {
	const when = longDate( date );
	const intro = [ sentence( `Checked ${ noDash( checked ) }` ), ...notes.map( noDash ) ];
	const md = [ `## Automated scan results: ${ when }`, ...intro ];
	const html = [ `<h2>Automated scan results: ${ when }</h2>`, ...intro.map( ( p ) => `<p>${ esc( p ) }</p>` ) ];
	for ( const g of GROUPS ) {
		const items = findings.filter( ( f ) => f.group === g.id );
		md.push( g.heading );
		html.push( `<p>${ g.heading }</p>` );
		if ( ! items.length ) {
			md.push( g.empty );
			html.push( `<p>${ g.empty }</p>` );
			continue;
		}
		md.push( items.map( ( f ) => `- ${ noDash( f.text ) } ${ f.url }` ).join( '\n' ) );
		html.push( `<ul>${ items.map( ( f ) => `<li>${ esc( noDash( f.text ) ) } <a href="${ esc( f.url ) }">${ esc( f.url ) }</a></li>` ).join( '' ) }</ul>` );
	}
	md.push( `End of automated scan results: ${ when }` );
	html.push( `<p>End of automated scan results: ${ when }</p>` );
	return { markdown: md.join( '\n\n' ) + '\n', html: html.join( '\n' ) };
}
