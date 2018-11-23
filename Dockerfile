FROM python:3-slim
MAINTAINER martin scharm <https://binfalse.de>

RUN pip install --no-cache-dir  argparse Mastodon.py sitemap_python

COPY mastodon-sitemap.py /mastodon-sitemap.py

ENTRYPOINT [ "python3", "/mastodon-sitemap.py" ]




