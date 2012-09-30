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

import unicodedata
from twikoto3 import codepoint
from twikoto3.twittertext import extractor

MAX_TWEET_LENGTH = 140;

shortUrlLength = 20;
shortUrlLengthHttps = 21;

def getTweetLength(text):
    text = unicodedata.normalize("NFC", text)
    length = len(codepoint.characters(text))

    for urlEntity in extractor.extractURLsWithIndices(text):
        length += urlEntity[1] - urlEntity[2]
        length += shortUrlLengthHttps if urlEntity[0].lower().startswith("https://") else shortUrlLength

    return length
