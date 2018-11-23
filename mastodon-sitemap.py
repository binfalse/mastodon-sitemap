
import sys
import argparse
from mastodon import Mastodon
import sitemap.generator as generator

# parse arguments
parser = argparse.ArgumentParser (description = 'Generate a sitemap of a mastodon user.')
parser.add_argument ('--instance', required=True, help='url to your instance')
parser.add_argument ('--access-token', required=True, help='token providing access to your account')
parser.add_argument ('--max-urls', type=int, default=1000, help='max number of urls to collect in the sitemap')
parser.add_argument ('file', metavar='FILE', nargs=1, help='file to store the sitemap')
args = parser.parse_args()

# sanitise arguments
if args.max_urls > 50000:
	# TODO support nested sitemaps...
	print ("there shouldn't be more than 50k urls in a sitemap!")
	sys.exit (1)


mstdn = Mastodon(
		access_token = args.access_token,
		api_base_url = args.instance
		)
user = mstdn.account_verify_credentials();


statuses = mstdn.account_statuses(user.id);



counter = 0

sitemap = generator.Sitemap()

sitemap.add(user.url,
            changefreq="hourly",
            priority="1.0")

while statuses and counter < args.max_urls:
	for status in statuses:
		if status.visibility != "public":
			continue
		counter += 1
		sitemap.add(status.url,
            lastmod=status.created_at)
		
		
		if counter >= args.max_urls:
			break
	statuses = mstdn.fetch_next(statuses)


sitemap_xml = sitemap.generate()
print (sitemap_xml)
