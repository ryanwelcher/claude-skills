<!-- requires: ste-pass -->
/ste-pass Make this short setup passage easier to follow for readers whose first language isn't English. It's from a Block Developer Cookbook recipe. Show me the findings only and do not ask me anything.

You can choose to either use the repository which provides a development environment or to just download the standalone plugin.

Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation.

    npx @wordpress/create-block@latest meme-generator --template @block-developer-cookbook/meme-generator

Once the scaffold has completed completed, start the build process from inside the newly created plugin

    cd meme-generator && npm run start

Finally, make sure to activate the plugin.
