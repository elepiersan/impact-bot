#!/usr/bin/env python
# coding: utf-8

import configparser
import os

here = os.path.abspath(os.path.dirname(__file__))
config = configparser.SafeConfigParser()
files = config.read([
    './impactbot.ini',
    os.path.join(here, 'impactbot.ini'),
    os.path.expanduser('~/impactbot.ini'),
    os.path.expanduser('~/.impactbot.rc')])

SLACK_TOKEN = config.get(
    'Slack', 'token',
    fallback=os.environ.get("SLACK_API_TOKEN", None))
