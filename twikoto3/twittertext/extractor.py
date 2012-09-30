# -*- coding: utf-8 -*-

"""
    twikoto3 - Twitter Client
    Copyright (C) 2012 azyobuzin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
    This file was transplanted from twitter-text-java.
    https://github.com/twitter/twitter-text-java
"""

from twikoto3.extension import *
from twikoto3.twittertext import regex

extractURLWithoutProtocol = True

def extractURLsWithIndices(text):
    urls = []

    if text | noneoremptystr() or ("." not in text if extractURLWithoutProtocol else ":" not in text):
        return urls

    for matcher in regex.VALID_URL.finditer(text):
        # skip if protocol is not present and 'extractURLWithoutProtocol' is false
        # or URL is preceded by invalid character.
        if not (matcher.group(regex.VALID_URL_GROUP_PROTOCOL) is None and (not extractURLWithoutProtocol or regex.INVALID_URL_WITHOUT_PROTOCOL_MATCH_BEGIN.search(matcher.group(regex.VALID_URL_GROUP_BEFORE)) is not None)):
            url = matcher.group(regex.VALID_URL_GROUP_URL)
            start = matcher.start(regex.VALID_URL_GROUP_URL)
            end = matcher.end(regex.VALID_URL_GROUP_URL)
            tco_matcher = regex.VALID_TCO_URL.match(url)
            if tco_matcher is not None:
                # In the case of t.co URLs, don't allow additional path characters.
                url = tco_matcher.group()
                end = start + len(url)

            urls.append((url, start, end))

    return urls
