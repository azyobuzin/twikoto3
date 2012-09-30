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

import re

LATIN_ACCENTS_CHARS = (
    "\\u00c0-\\u00d6\\u00d8-\\u00f6\\u00f8-\\u00ff" + # Latin-1
    "\\u0100-\\u024f" + # Latin Extended A and B
    "\\u0253\\u0254\\u0256\\u0257\\u0259\\u025b\\u0263\\u0268\\u026f\\u0272\\u0289\\u028b" + # IPA Extensions
    "\\u02bb" + # Hawaiian
    "\\u0300-\\u036f" + # Combining diacritics
    "\\u1e00-\\u1eff" # Latin Extended Additional (mostly for Vietnamese)
)

URL_VALID_PRECEEDING_CHARS = "(?:[^A-Z0-9@＠$#＃\u202A-\u202E]|^)"

URL_VALID_CHARS = "a-zA-Z0-9" + LATIN_ACCENTS_CHARS
URL_VALID_SUBDOMAIN = "(?:(?:[" + URL_VALID_CHARS + "][" + URL_VALID_CHARS + "\\-_]*)?[" + URL_VALID_CHARS + "]\\.)"
URL_VALID_DOMAIN_NAME = "(?:(?:[" + URL_VALID_CHARS + "][" + URL_VALID_CHARS + "\\-]*)?[" + URL_VALID_CHARS + "]\\.)"
#Any non-space, non-punctuation characters. \p{Z} = any kind of whitespace or invisible separator.
URL_VALID_UNICODE_CHARS = "[^!\\\"#\\$%&'\\(\\)\\*\\+,\\-\\./:;<=>\\?@\\[\\]\\^_`\\{\\|\\}~\\s\\u2000-\\u206F]"

URL_VALID_GTLD = "(?:(?:aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|xxx)(?=[^a-zA-Z0-9]|$))"
URL_VALID_CCTLD = "(?:(?:ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|ss|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw)(?=[^a-zA-Z0-9]|$))"
URL_PUNYCODE = "(?:xn--[0-9a-z]+)"

URL_VALID_DOMAIN = (
    "(?:" +                                                   # subdomains + domain + TLD
        URL_VALID_SUBDOMAIN + "+" + URL_VALID_DOMAIN_NAME +   #// e.g. www.twitter.com, foo.co.jp, bar.co.uk
        "(?:" + URL_VALID_GTLD + "|" + URL_VALID_CCTLD + "|" + URL_PUNYCODE + ")" +
      ")" +
    "|(?:" +                                                  # domain + gTLD
      URL_VALID_DOMAIN_NAME +                                 # e.g. twitter.com
      "(?:" + URL_VALID_GTLD + "|" + URL_PUNYCODE + ")" +
    ")" +
    "|(?:" + "(?:(?<=http://)|(?<=https://))" +
      "(?:" +
        "(?:" + URL_VALID_DOMAIN_NAME + URL_VALID_CCTLD + ")" +  # protocol + domain + ccTLD
        "|(?:" +
          URL_VALID_UNICODE_CHARS + "+\\." +                     # protocol + unicode domain + TLD
          "(?:" + URL_VALID_GTLD + "|" + URL_VALID_CCTLD + ")" +
        ")" +
      ")" +
    ")" +
    "|(?:" +                                                  # domain + ccTLD + '/'
      URL_VALID_DOMAIN_NAME + URL_VALID_CCTLD + "(?=/)" +     # e.g. t.co/
    ")"
)

URL_VALID_PORT_NUMBER = "[0-9]+"

URL_VALID_GENERAL_PATH_CHARS = "[a-z0-9!\\*';:=\\+,\\.\\$/%#\\[\\]\\-_~\\|&" + LATIN_ACCENTS_CHARS + "]"
"""
    Allow URL paths to contain balanced parens
    1. Used in Wikipedia URLs like /Primer_(film)
    2. Used in IIS sessions like /S(dfd346)/
"""
URL_BALANCED_PARENS = "\\(" + URL_VALID_GENERAL_PATH_CHARS + "+\\)"
"""
    Valid end-of-path chracters (so /foo. does not gobble the period).
    2. Allow =&# for empty URL parameters and other URL-join artifacts
"""
URL_VALID_PATH_ENDING_CHARS = "[a-z0-9=_#/\\-\\+" + LATIN_ACCENTS_CHARS + "]|(?:" + URL_BALANCED_PARENS +")"

URL_VALID_PATH = (
  "(?:" +
    "(?:" +
      URL_VALID_GENERAL_PATH_CHARS + "*" +
      "(?:" + URL_BALANCED_PARENS + URL_VALID_GENERAL_PATH_CHARS + "*)*" +
      URL_VALID_PATH_ENDING_CHARS +
    ")|(?:@" + URL_VALID_GENERAL_PATH_CHARS + "+/)" +
  ")"
)

URL_VALID_URL_QUERY_CHARS = "[a-z0-9!?\\*'\\(\\);:&=\\+\\$/%#\\[\\]\\-_\\.,~\\|]"
URL_VALID_URL_QUERY_ENDING_CHARS = "[a-z0-9_&=#/]"
VALID_URL_PATTERN_STRING = (
  "(" +                                                            #  $1 total match
    "(" + URL_VALID_PRECEEDING_CHARS + ")" +                       #  $2 Preceeding chracter
    "(" +                                                          #  $3 URL
      "(https?://)?" +                                             #  $4 Protocol (optional)
      "(" + URL_VALID_DOMAIN + ")" +                               #  $5 Domain(s)
      "(?::(" + URL_VALID_PORT_NUMBER +"))?" +                     #  $6 Port number (optional)
      "(/" +
        URL_VALID_PATH + "*" +
      ")?" +                                                       #  $7 URL Path and anchor
      "(\\?" + URL_VALID_URL_QUERY_CHARS + "*" +                   #  $8 Query String
              URL_VALID_URL_QUERY_ENDING_CHARS + ")?" +
    ")" +
  ")"
)

VALID_URL = re.compile(VALID_URL_PATTERN_STRING, re.IGNORECASE)
VALID_URL_GROUP_ALL          = 1
VALID_URL_GROUP_BEFORE       = 2
VALID_URL_GROUP_URL          = 3
VALID_URL_GROUP_PROTOCOL     = 4
VALID_URL_GROUP_DOMAIN       = 5
VALID_URL_GROUP_PORT         = 6
VALID_URL_GROUP_PATH         = 7
VALID_URL_GROUP_QUERY_STRING = 8

VALID_TCO_URL = re.compile("^https?:\\/\\/t\\.co\\/[a-z0-9]+", re.IGNORECASE)
INVALID_URL_WITHOUT_PROTOCOL_MATCH_BEGIN = re.compile("[-_./]$")
