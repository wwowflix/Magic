# -*- coding: utf-8 -*-
import praw

reddit = praw.Reddit(
    client_id="OBhDPCPwu_CJkw813LQwng",
    client_secret="zjl6-I2sU9i3cNOBRx76tnpLCyPCBg",
    user_agent="MAGICZephyrScraper/0.1 by u/AffectionateRoom6084",
    username="AffectionateRoom6084",
    password="Hpdv2000",
)

print(reddit.user.me())
