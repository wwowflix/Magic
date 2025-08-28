# -*- coding: utf-8 -*-
from TikTokApi import TikTokApi
import asyncio
import pprint


async def main():
    api = TikTokApi()
    await api.create_sessions()
    trending = api.trending()
    async for video in trending.videos():
        data = video.as_dict  # raw dict of all fields
        pprint.pprint(data)  # pretty-print it
        break  # just the first one


asyncio.run(main())
