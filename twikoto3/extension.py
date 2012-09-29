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

class Extension:
    def __init__(self, action):
        self.action = action

    def __ror__(self, source):
        return self.action(source)

def let(action):
    return Extension(action)

def apply(action):
    def handler(source):
        action(source)
        return source

    return Extension(handler)

def noneoremptystr():
    return Extension(lambda str: str is None or str == "")

def none(defaultvalue):
    return Extension(lambda obj: obj if obj is not None else defaultvalue)
