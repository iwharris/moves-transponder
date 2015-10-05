# moves-transponder

A connector for the Moves app that reports the last known location of a certain user. It is written as a Google App Engine app.

##Acknowlegements

This makes use of the [moves-fetch](https://gist.github.com/KainokiKaede/7264280) gist written by [KainokiKaede](https://gist.github.com/KainokiKaede).

##Usage

###Authorization

You will first need to register a new app on [moves-app.com](https://dev.moves-app.com/apps). Enter any metadata you want. Under the "Development" tab in the "Redirect URI" field, put any value (I use "localhost").

After registering the app, you will receive a Client ID and Client Secret.