# Mastodon Sitemap Generator

This is a [Python](https://www.python.org/) tool to generate an [XML sitemap](https://en.wikipedia.org/wiki/Sitemaps) for a single [Mastodon](https://en.wikipedia.org/wiki/Mastodon_(software)) account.
It is, thus, primarily made for single-user installations.
If your on a multiuser instance, you can still create your sitemap. You just cannot put it in the webservers root directory.. (maybe you have some other place to point search engines to it..?)
In general, it would also be possible to create an individual sitemap per user and have a sitemap index listing all user-specific sitemaps..
However, even that would probably only be feasible on instances with just a few users...


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

In that account, you need to create a new application.
From the web backend click `Preferences` -> `Development` -> `new application` and give it a name and a website (doesn't actually matter..).
It is sufficient to give it permissions to `read` and `read:statuses`, any other permissions (write, follow, ...)_are not required.

Save the changes and click your new application.
On the top of the applications page it will list some cryptic strings.
For the sitemap generator you'll need `Your access token`.


## Usage

The sitemap generator accepts the following arguments:

* `--instance URL` the URL to your Mastodon instance, for example `https://mstdn.binfalse.de`
* `--access-token TOKEN` the cryptic string from the application that you created in your Mastodon backend
* `--max-urls NUM` the number of urls to include in the sitemap (defaults to 1000)
* `--overwrite` to force the generator to overwrite the sitemap file if it already exists
* and finally the file in which to store the sitemap (use `-` to print the sitemap to std out)

To generate a sitemap you would for example call:

    python3 mastodon-sitemap.py --instance https://mstdn.binfalse.de --access-token f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2 --max-urls 50 --overwrite /tmp/sitemap.xml

and a few seconds later you'll hopefully find you sitemap with 50 urls (max) in `/tmp/sitemap.xml`!



## Multiuser Instances

If you're a user on a multiuser instance, you can of course still generate your sitemap.
You just cannot put the sitemap on the root of the webserver..
Not sure if it can still be useful for you? You may 




