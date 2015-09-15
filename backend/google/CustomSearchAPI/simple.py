

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.
Command-line application that does a search.
"""

__author__ = 'shyu'

import pprint

from googleapiclient.discovery import build


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyDkxRofVDMMrci34b9yFCePgJz2YAoDmAA")


  #  https://developers.google.com/custom-search/json-api/v1/reference/cse/list
  res = service.cse().list(
      q='Olympics',
      cx='012608441591405123751:clhx3wq8jxk',
      num=10,
      start=11,
      dateRestrict='y1',
      #lr='lang_zh-CN',
      #searchType='image',
    ).execute()
  pprint.pprint(res)

if __name__ == '__main__':
  main()