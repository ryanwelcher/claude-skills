# Meme Generator

In this recipe, we're building a meme generator block. It pulls meme templates from a third-party API and lets people add their own text, and then we'll register a font collection so the punchline actually looks like a meme. This one's a lot of fun.

## Setup

The scaffold gives you a working block with the attributes and helper components already in place, so you can spend your time on the fun parts.

**Requirements:**

- A local WordPress site.
- Node.js, version 20 or higher.

1. Open a terminal.
2. Go to the `plugins` folder of your local WordPress site.
3. Type this command:

   ```bash
   npx @wordpress/create-block@latest meme-generator --template @block-developer-cookbook/meme-generator
   ```

4. Go to the new plugin folder and start the build:

   ```bash
   cd meme-generator && npm run start
   ```

5. In the WordPress admin area, activate the **Meme Generator** plugin.

## Step 3 – Getting the images

Memes live and die by their images, and I didn't want to hand-curate a list. Imgflip has a public endpoint that returns the most popular meme templates, so we'll lean on that. The request itself is easy. The tricky part is making sure React doesn't fire it a few thousand times.

The `useEffect` hook runs code after React shows the component. Its dependency array controls when the hook runs again.

| Dependency array | When the hook runs |
|---|---|
| Not given | After each change to the component |
| `[]` (empty) | One time, when the component is first shown |

**CAUTION:** Do not put the `fetch` call directly in the `Edit` function. React runs `Edit` each time the block changes, so the browser can stop.

1. Open `src/edit.js`.
2. Below `useBlockProps()`, add this code:

   ```js
   const [ allImages, setAllImages ] = useState( [] );

   useEffect( () => {
       const loadImages = async () => {
           const response = await fetch( 'https://api.imgflip.com/get_memes' );
           const { success, data } = await response.json();
           if ( success ) {
               setAllImages( data.memes );
           }
       };
       loadImages();
   }, [] );
   ```

3. Save the file.
4. Refresh the editor and open the browser console.
5. Make sure that the request runs only one time.

**NOTE:** You can't make the `useEffect` callback itself `async`. Define an `async` function inside it, then call that function.

## Step 9 – Meme fonts

Part of what makes memes great is the font. Nobody takes a meme seriously in Times New Roman. A plugin can't install fonts for you, but it can offer a collection that people install in a couple of clicks, and I think that's the nicer experience anyway.

1. Open `meme-generator.php`.
2. Inside the `init` hook callback, below `register_block_type()`, add this code:

   ```php
   wp_register_font_collection( 'memes', [
       'name'          => __( 'Meme fonts', 'meme-generator' ),
       'description'   => __( 'For the LOLZ!', 'meme-generator' ),
       'font_families' => [
           [
               'font_family_settings' => [
                   'fontFamily' => "'Impact', sans-serif",
                   'slug'       => 'impact',
                   'name'       => __( 'Impact', 'meme-generator' ),
               ],
               'categories' => [ 'memes' ],
           ],
       ],
       'categories'    => [
           [ 'name' => __( 'Memes', 'meme-generator' ), 'slug' => 'memes' ],
       ],
   ] );
   ```

3. Save the file.
4. Go to **Appearance > Editor > Styles > Typography**.
5. Open the font library and select the **Meme fonts** collection.
6. Install the **Impact** font.
7. Make sure that **Impact** shows in the block's typography controls.

| Problem | Possible cause | Action |
|---|---|---|
| The collection does not show. | The plugin is not active. | Activate the plugin. |
| The font does not show in the block. | The font is not installed. | Install the font from the font library. |

And that's kind of it. If you build something ridiculous with this, I want to see it.
