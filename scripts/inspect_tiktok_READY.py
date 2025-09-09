# -*- coding: utf-8 -*-
import asyncio
import pprint

from TikTokApi import TikTokApi


async def main():
    api = TikTokApi()
    await api.create_sessions()
    trending = api.trending()
    async for video in trending.videos():
        data = video.as_dict  # raw dict of all fields
        pprint.pprint(data)  # pretty-print it
        break  # just the first one


asyncio.run(main())
