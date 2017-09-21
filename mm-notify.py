#!/usr/bin/env python2

# Copyright (c) 2017 Maxim Odinintsev
#
# Based on Nagios notification plugin by NDrive
# https://github.com/NDrive/nagios-mattermost
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import json
try:
    import urllib2  # python2
except ModuleNotFoundError:
    import urllib.request as urllib2  # python3
import os

VERSION = "0.0.1"


def parse():
    parser = argparse.ArgumentParser(description='Sends alerts to Mattermost')
    parser.add_argument('--url', help='Incoming Webhook URL', required=True)
    parser.add_argument('--channel', help='Channel to notify')
    parser.add_argument('--username', help='Username to notify as',
                        default='m/monit notify')
    parser.add_argument('--iconurl', help='URL of icon to use for username',
                        default='https://mmonit.com/monit/img/logo.png')  # noqa
    parser.add_argument('--notificationtype', help='Notification Type',
                        default='none')
    parser.add_argument('--version', action='version',
                        version='% (prog)s {version}'.format(version=VERSION))
    args = parser.parse_args()
    return args


def encode_special_characters(text):
    text = text.replace("%", "%25")
    return text


def make_data(args):
    template = "**{action}**\n" \
               "**{event}**\n\n" \
               "Host affected: **{host}**\n" \
               "Service affected: **{service}**\n" \
               "Details: {details}" \
               .format(action=os.environ['MONIT_ACTION'],
                       event=os.environ['MONIT_EVENT'],
                       host=os.environ['MONIT_HOST'],
                       service=os.environ['MONIT_SERVICE'],
                       details=os.environ['MONIT_DESCRIPTION'])

    # Emojis
    print(args.notificationtype.lower())
    if args.notificationtype.lower() == "alert":
        EMOJI = ":sos: "
    elif args.notificationtype.lower() == "stop":
        EMOJI = ":red_circle: "
    elif args.notificationtype.lower() == "start":
        EMOJI = ":white_check_mark: "
    elif args.notificationtype.lower() == "restart":
        EMOJI = ":arrows_counterclockwise: "
    elif args.notificationtype.lower() == "exec":
        EMOJI = ":interrobang: "
    elif args.notificationtype.lower() == "unmonitor":
        EMOJI = ":heavy_exclamation_mark: "
    else:
        EMOJI = ""

    text = EMOJI + template.format(**vars(args))

    payload = {
        "username": args.username,
        "icon_url": args.iconurl,
        "text": encode_special_characters(text)
    }

    if args.channel:
        payload["channel"] = args.channel

    data = "payload=" + json.dumps(payload)
    return data


def request(url, data):
    binary_data = data.encode('ascii')
    req = urllib2.Request(url, binary_data)
    response = urllib2.urlopen(req)
    return response.read()


if __name__ == "__main__":
    args = parse()
    data = make_data(args)
    response = request(args.url, data)
    print(response)
