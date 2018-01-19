#!/usr/bin/env python
# coding: utf-8

from functools import lru_cache

from slackclient import SlackClient

from config import SLACK_TOKEN


class SlackPoster:
    def __init__(self, token, channels):
        self.client = SlackClient(token)
        self.channels = channels

    def post(self, message):
        for ch in self.channels:
            self.client.api_call(
                'chat.postMessage',
                channel=ch,
                text=message,
                as_user=False,
                username='impactbot',
                icon_emoji=':star2:'
            )

@lru_cache()
def make_post_function(channels):
    sp = SlackPoster(SLACK_TOKEN, channels)
    return sp.post


def post_to_slack(message, channels):
    poster = make_post_function(channels)
    poster(message)
