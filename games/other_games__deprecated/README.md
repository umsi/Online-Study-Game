# Deprecation warning!

Functionality in the `other_games__deprecated` app is *untested* and *unmigrated*.

Previously this code lived in a shared app, but was apparently unused. It was relocated to a catchall app here in order to simplify and debug the main `invest_game` app.

Functionality in this app could be restored in the future if needed, but would require wiring up urls, testing views and models, and running a database migration.
