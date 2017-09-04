## Map of the Crosswalk Survey ##

This is my first time messing with Heroku/[Dokku](http://dokku.viewdocs.io/dokku/), so things are very very rough.

This is a simple app to show some of the logged data from a [KoBoToolbox](http://www.kobotoolbox.org/) survey that's in progress. It's written in Python 3.

### Running this ###
If you want to run this at home, and you're on Windows, you'll have to figure out how to install [Memcached](http://memcached.org/), and then set the following environment variables:

* MEMCACHED_URL to "memcached://[your ip, or localhost]:[memcached port, maybe 11211]"
* KOBO_FORMID to the id of the Kobo survey you're pointing at (keep in mind the app is pretty much hardcoded to a particular survey at the moment!) You can find this looking at the [Kobo API](https://kc.kobotoolbox.org/api/v1/data), it's the "pk" thing needed to get submitted data for a form
* KOBO_USER to the username of the Kobo account
* KOBO_PASS to the password of the Kobo account

If you want to run this on Dokku, here are the server setup commands:
* `dokku apps:create <appname>`
* `dokku config:set <appname> KOBO_FORMID=<...> KOBO_USER=<...> KOBO_PASS=<...>`
* `sudo dokku plugin:install https://github.com/dokku/dokku-memcached.git memcached`
* `dokku memcached:create <backendname>`
* `dokku memcached:link <backendname> <appname>`

where the environment variables are the same as above. After that, push to deploy!
