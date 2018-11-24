# Mastodon Sitemap Generator

This is a [Python](https://www.python.org/) tool to generate an [XML sitemap](https://en.wikipedia.org/wiki/Sitemaps) for [Mastodon](https://en.wikipedia.org/wiki/Mastodon_(software)).
By default, it will create a sitemap for a specific user, but it can as well be used to generate a sitemap for the toots of all local users.



## Requirements

### Python

You need to have python 3 with the following packages installed:

* [argparse](https://docs.python.org/3/library/argparse.html)
* [Mastodon.py](https://github.com/halcy/Mastodon.py)
* [sitemap_python](https://github.com/socrateslee/sitemap_python)

To install the dependencies using pip, you would need to call

    pip3 install argparse Mastodon.py sitemap_python


### Mastodon

Of course, you need a Mastodon account... ;-)

In that account, you need to create a new application. From the web backend click `Preferences` -> `Development` -> `new application` and give it a name and a website (doesn't actually matter..). It is sufficient to give it permissions to `read` and `read:statuses`, any other permissions (write, follow, ...) are not required.

Save the changes and click your new application. On the top of the applications page it will list some cryptic strings. For the sitemap generator you'll need `Your access token`.


## Usage

The sitemap generator accepts the following arguments:

* `--instance URL` the URL to your Mastodon instance, for example `https://mstdn.binfalse.de`
* `--access-token TOKEN` the cryptic string from the application that you created in your Mastodon backend
* `--max-urls NUM` the number of urls to include in the sitemap (defaults to 1000)
* `--overwrite` to force the generator to overwrite the sitemap file if it already exists
* `--whole-instance` will create a sitemap for the whole instance (otherwise you'll get a sitemap for the toots of the current user), this sitemap will contain the latest toots from the local timeline and the distinct users who wrote it
* `--proper-lastmod` properly check when a toot-page was last modified (aka when was the last reply to that toot? by default we set lastmod to the creation date of the toot) - please keep in mind, that this *significantly increases the performance,* as we need an extra API call for every single toot!
* and finally the file in which to store the sitemap (use `-` to print the sitemap to std out)

To generate a sitemap you would for example call:

    python3 mastodon-sitemap.py --instance https://mstdn.binfalse.de        \
                                --access-token f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2 \
                                --max-urls 50                               \
                                --overwrite                                 \
                                /tmp/sitemap.xml

and a few seconds later you'll hopefully find you sitemap with 50 urls (max) in `/tmp/sitemap.xml`!

Put that in a cron job and your sitemap will stay up-to-date :)


### Docker

There is a Docker image available at [binfalse/mastodon-sitemap](https://hub.docker.com/r/binfalse/mastodon-sitemap/). It basically supports the same options, you just need to mount the destination directory into the container.

To generate a sitemap in `/path/to/sitemap.xml` you would call:

     docker run --rm -ti -v /path/to:/stuff binfalse/mastodon-sitemap                           \
                --instance https://mstdn.binfalse.de                                            \
                --access-token f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2 \
                --overwrite                                                                     \
                /stuff/sitemap.xml




## License

        mastodon-sitemap is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with PyThumb.  If not, see <http://www.gnu.org/licenses/>.




