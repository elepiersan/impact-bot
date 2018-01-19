#!/usr/bin/env python
# coding: utf-8

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


def post_to_slack(message, channels):
    global _poster
    if _poster is None:
        _poster = SlackPoster(SLACK_TOKEN, channels)
    sp.post(message)
