# The MIT License (MIT)
#
# Copyright (c) 2016 Yutkin Dmitry
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

VKAPI_URL = 'https://api.vk.com/method/'
VKAPI_VERSION = 5.53

TXT_ID_PTRN = r'(?:https?:\/\/)(?:vk.com\/(?!club|public|id|event))' \
              r'(?P<id>(?![_.])(?!club|public|id|event)[a-z0-9_.]*' \
              r'[a-z][a-z0-9_.]*)'
NUM_ID_PTRN = r'^(?:https?:\/\/)?(?:vk.com\/)?(?P<type>club|public|id|event)' \
              r'(?P<id>\d+)$'

TXT_ID_REGEXP = re.compile(TXT_ID_PTRN)
NUM_ID_REGEXP = re.compile(NUM_ID_PTRN)
