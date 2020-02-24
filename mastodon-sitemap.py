#!/usr/bin/env python3
# encoding=utf8
#
# Copyright 2018 Martin Scharm <https://binfalse.de/contact/>
#
# This file is part of mastodon-sitemap.
# <https://github.com/binfalse/mastodon-sitemap/>
#
# mastodon-sitemap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mastodon-sitemap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mastodon-sitemap.  If not, see <http://www.gnu.org/licenses/>.

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
parser.add_argument ('--proper-lastmod', action='store_true', help='properly check when a toot-page was last modified (aka when was the last reply to that toot?) - please keep in mind, that this significantly increases the performance, as we need an extra API call for every single toot!')
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
if filename != "-" and os.path.isfile (filename) and not args.overwrite:
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
sitemap.add(args.instance,
            changefreq="monthly",
            priority="0.9")
sitemap.add(user.url,
            changefreq="hourly",
            priority="1.0")

users = [user.url]

# collect first bunch of toots
if args.whole_instance:
    toots = mstdn.timeline_local ();
else:
    toots = mstdn.account_statuses (user.id);
counter = 2

# iterate toots
while toots and counter < args.max_urls:
	for toot in toots:
		# only consider public toots
		if toot.reblog or toot.visibility != "public":
			continue
		
		# find when it was last modified
		lm = toot.created_at
		if args.proper_lastmod:
			context = mstdn.status_context (toot.id)
			if context.descendants:
				for desc in context.descendants:
					if lm < desc.created_at:
						lm = desc.created_at
		
		# add to sitemap
		sitemap.add(toot.url, lastmod=lm.isoformat())
		counter += 1
		
		if toot.account.url not in users:
			users.append (toot.account.url)
			sitemap.add(toot.account.url, priority = "0.9", changefreq="hourly")
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
if filename == "-":
	print (sitemap_xml)
else:
	with open (filename, 'w') as f:
		f.write (sitemap_xml)


