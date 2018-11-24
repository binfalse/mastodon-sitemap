#!/usr/bin/env python3
import os
import sys
import argparse
from mastodon import Mastodon
import sitemap.generator as generator

# parse arguments
parser = argparse.ArgumentParser (description = 'Generate a sitemap of a mastodon user.')
parser.add_argument ('--instance', required=True, help='url to your instance')
parser.add_argument ('--access-token', required=True, help='token providing access to your account')
parser.add_argument ('--max-urls', type=int, default=1000, help='max number of urls to collect in the sitemap')
parser.add_argument ('--overwrite', action='store_true', help='overwrite sitemap if it exists')
parser.add_argument ('--whole-instance', action='store_true', help='create sitemap for all users on that instance')
parser.add_argument ('file', metavar='FILE', help='file to store the sitemap, use - for std out')
args = parser.parse_args()


# sanitise arguments

if args.max_urls > 50000:
	# TODO support nested sitemaps...
	print ("there shouldn't be more than 50k urls in a sitemap!")
	sys.exit (1)
if args.max_urls < 1:
	# TODO support nested sitemaps...
	print ("no urls no sitemap")
	sys.exit (1)

filename = args.file
if filename is not "-" and os.path.isfile (filename) and not args.overwrite:
	print ("sitemap " + args.file + " exists, will not overwrite it")
	sys.exit (1)




# connect to mastodon
mstdn = Mastodon(
		access_token = args.access_token,
		api_base_url = args.instance
		)
user = mstdn.account_verify_credentials();


# start a sitemap
sitemap = generator.Sitemap()
# add the user's main page
sitemap.add(user.url,
            changefreq="hourly",
            priority="1.0")

# collect first bunch of toots
if args.whole_instance:
    toots = mstdn.timeline_local ();
else:
    toots = mstdn.account_statuses (user.id);
counter = 1

# iterate toots
while toots and counter < args.max_urls:
	for toot in toots:
		# only consider public toots
		if toot.visibility != "public":
			continue
		
		# add to sitemap
		sitemap.add(toot.url, lastmod=toot.created_at.isoformat())
		counter += 1
		
		# break if we saw enough...
		if counter >= args.max_urls:
			break
		
	# fetch new toots if necessary
	if counter < args.max_urls:
		toots = mstdn.fetch_next(toots)

# generate sitemap
sitemap_xml = sitemap.generate()

# export sitemap
if filename is "-":
	print (sitemap_xml)
else:
	with open (filename, 'w') as f:
		f.write (sitemap_xml)


