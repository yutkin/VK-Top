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

import requests

from . import constants

class VKApiError(RuntimeError):
  pass

def get_page_id(url):
  """ Returns page's numeric ID """
  params = {'screen_name': url['id'], 'v': constants.VKAPI_VERSION}
  if url['type'] == 'domain':
    request = requests.get(constants.VKAPI_URL + 'utils.resolveScreenName',
                           params=params)
    response = request.json()['response']

    if response:
      if response['type'] == 'user':
        return response['object_id']
      else:
        return -response['object_id']
    else:
      raise RuntimeError('Troubles with resolving {} id'.format(url['id']))

  id = int(url['id'])
  return id if url['type'] == 'id' else -id

def pretty_print(posts, col_indent_len=6):
  """ Prints results as a pretty table """

  if not posts:
    print('There are no any posts for showing.')
    return

  longest_url_len = max([len(post.url) for post in posts])
  longest_likes_len = max([len(str(post.likes)) for post in posts])
  longest_reposts_len = max([len(str(post.reposts)) for post in posts])


  # This header print was hardcoded and cannot be properly explained. :(
  # But it adjusts to col_indent_len parameter.
  print('\n{0:^{4}} {1:^{5}} {2:^{6}} {3:^{7}}'.format('URL', 'Date', 'Likes', 'Reposts',
                                      longest_url_len+4,
                                      2*col_indent_len + 10,
                                      longest_likes_len,
                                      2*col_indent_len+longest_reposts_len-1
                                      ))
  for i, post in enumerate(posts):
    data = {
      'ind': str(i+1) + '.',
      'url': post.url,
      'likes': post.likes,
      'reposts': post.reposts,
      'url_len': longest_url_len + col_indent_len,
      'likes_len': longest_likes_len + col_indent_len,
      'reposts_len': longest_reposts_len + col_indent_len,
      'date': post.date,
      'date_len': col_indent_len + 10,
    }
    print('{ind:<3} {url:<{url_len}} {date!s:<{date_len}} {likes:<{likes_len}}'
          '{reposts:<{reposts_len}}'.format(**data))
