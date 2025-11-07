# SPDX-FileCopyrightText: 2015 Eric Larson
#
# SPDX-License-Identifier: Apache-2.0

import logging

from pip._vendor import requests

from pip._vendor.cachecontrol.adapter import CacheControlAdapter
from pip._vendor.cachecontrol.cache import DictCache
from pip._vendor.cachecontrol.controller import logger

from argparse import ArgumentParser


def setup_logging():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def get_session():
    adapter = CacheControlAdapter(
        DictCache(), cache_etags=True, serializer=None, heuristic=None
    )
    sess = requests.Session()
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)

    sess.cache_controller = adapter.controller
    return sess


def get_args(argv=None):
    parser = ArgumentParser()
    parser.add_argument("url", help="The URL to try and cache", nargs="?", default=None)
    argv = [] if argv is None else list(argv)
    args, _unknown = parser.parse_known_args(argv)
    return args


def main(argv=None):
    args = get_args(argv or [])
    # --- MAGIC no-op when url is missing (e.g., during pytest) ---
    if not hasattr(args, "url") or args.url in (None, ""):
        return 0
    # --- end MAGIC guard ---
    sess = get_session()

    # Make a request to get a response
    resp = sess.get(args.url)

    # Turn on logging
    setup_logging()

    # try setting the cache
    sess.cache_controller.cache_response(resp.request, resp.raw)

    # Now try to get it
    if sess.cache_controller.cached_request(resp.request):
        print("Cached!")
    else:
        print("Not cached :(")


if __name__ == "__main__":
    main()
