/**
 * Layout check for a deck built from templates/deck.html.
 *
 * Serve the deck folder over HTTP (for example `python3 -m http.server 8765`), open the
 * deck in Chrome, and run this in the page (DevTools console, or a browser tool's
 * JavaScript runner). It loads the deck in fixed-size frames, shows every build step, and
 * reports each slide whose content runs off the slide or whose code block scrolls.
 *
 * Result: { "1280x720": {}, ... } means every slide fits at that size. Otherwise each
 * problem slide is listed by number with how many pixels overflow:
 *   v = off the bottom, h = off the right, pre = code block scrolling.
 */
( async () => {
	const sizes = [
		[ 1920, 1080 ],
		[ 1440, 810 ],
		[ 1366, 768 ],
		[ 1280, 720 ], // smallest common 16:9 projector
		[ 1280, 800 ], // 16:10
	];
	const report = {};
	for ( const [ w, h ] of sizes ) {
		const frame = document.createElement( 'iframe' );
		frame.style.cssText = `position:fixed;left:0;top:0;width:${ w }px;height:${ h }px;border:0;opacity:0.01;z-index:99999`;
		frame.src = location.pathname + '?layout-check=' + Math.random() + '#1';
		document.documentElement.appendChild( frame );
		await new Promise( ( resolve ) => ( frame.onload = resolve ) );
		await new Promise( ( resolve ) => setTimeout( resolve, 600 ) );
		const doc = frame.contentDocument;
		const win = frame.contentWindow;
		// Show every build step; hidden bullets keep their space, so they need no change.
		doc.head.insertAdjacentHTML(
			'beforeend',
			'<style>[data-frag]{opacity:1!important;visibility:visible!important}</style>'
		);
		const slides = [ ...doc.querySelectorAll( 'section.slide' ) ];
		const problems = {};
		slides.forEach( ( slide, i ) => {
			slides.forEach( ( s ) => s.classList.remove( 'current' ) );
			slide.classList.add( 'current' );
			const box = slide.getBoundingClientRect();
			let v = 0;
			let hOver = 0;
			let pre = 0;
			slide.querySelectorAll( '*' ).forEach( ( el ) => {
				if ( el.closest( 'pre' ) ) {
					return;
				}
				const r = el.getBoundingClientRect();
				if ( ! r.width ) {
					return;
				}
				v = Math.max( v, r.bottom - Math.min( box.bottom, win.innerHeight ) );
				hOver = Math.max( hOver, r.right - Math.min( box.right, win.innerWidth ) );
			} );
			slide.querySelectorAll( 'pre' ).forEach( ( p ) => {
				pre = Math.max( pre, p.scrollWidth - p.clientWidth, p.scrollHeight - p.clientHeight );
			} );
			if ( v > 1 || hOver > 1 || pre > 2 ) {
				problems[ i + 1 ] = { v: Math.round( v ), h: Math.round( hOver ), pre };
			}
		} );
		report[ `${ w }x${ h }` ] = problems;
		frame.remove();
	}
	console.log( JSON.stringify( report, null, 1 ) );
	return report;
} )();
