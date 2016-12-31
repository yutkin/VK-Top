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

from __future__ import print_function

import requests
import sys
import datetime
from datetime import timedelta

from .argparser import parse_args
from .constants import VKAPI_URL, VKAPI_VERSION
from .utils import get_page_id, VKApiError, pretty_print
from .post import Post

# Define logging parameters for --verbose option
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[\033[92m%(levelname)s %(asctime)s\033[0m]: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# Removing noisy debug messages from lib request
requests_logger = logging.getLogger('requests')
requests_logger.setLevel(logging.CRITICAL)
LOGGER = logging.getLogger()

class PostDownloader:
  def __init__(self, page_id, from_date=None, to_date=None):
    self.page_id = page_id
    self.api_url = VKAPI_URL + 'wall.get'
    self.request_params = {'owner_id': self.page_id, 'v': VKAPI_VERSION}
    self.from_date = from_date or datetime.date.min
    self.to_date = to_date or datetime.date.max
  
  def _number_of_posts(self):
    """ Returns total number of post on the page """

    self.request_params['offset'] = 0
    self.request_params['count'] = 1
    
    response = requests.get(self.api_url, params=self.request_params).json()
    
    if 'error' in response:
      raise VKApiError(response['error']['error_msg'])
    
    return response['response']['count']
  
  def fetch(self, init_offset=0, num_to_fetch=None, verbose_mode=False):
    """ Downloads 'num_to_fetch' posts starting from 'init_offset' position """

    from multiprocessing import current_process
    global LOGGER

    num_to_fetch = num_to_fetch or self._number_of_posts()
    self.request_params['offset'] = init_offset
    self.request_params['count'] = min(num_to_fetch, 100)

    if verbose_mode:
      LOGGER.debug('{} trying to download {} posts'.format(current_process().name,
                                                           num_to_fetch))

    fetched_posts = []
    fetched_counter = 0
    while fetched_counter != num_to_fetch:
      response = requests.get(self.api_url, params=self.request_params).json()
    
      if 'error' in response:
        raise VKApiError(response['error']['error_msg'])
      
      posts = response['response']['items']
      fetched_counter += len(posts)

      if verbose_mode:
        LOGGER.debug('{} downloaded {}/{} posts'.format(current_process().name,
                                                 fetched_counter, num_to_fetch))

      for post in posts:
        post = Post(
          id=post['id'],
          text=post['text'],
          likes=post['likes']['count'],
          reposts=post['reposts']['count'],
          date=datetime.date.fromtimestamp(post['date']),
          url='https://vk.com/wall{0}_{1}'.format(self.page_id, post['id'])
        )
        if self.from_date <= post.date <= self.to_date:
          fetched_posts.append(post)

        # Early stopping, all subsequent post should be discarded
        elif post.date < self.from_date:
          if verbose_mode:
            LOGGER.debug('{} returns eventually {} posts'.format(
              current_process().name, len(fetched_posts)))
          return fetched_posts

      self.request_params['offset'] += 100
      self.request_params['count'] = min(num_to_fetch - fetched_counter, 100)

    if verbose_mode:
      LOGGER.debug('{} returns eventually {} posts'.format(
        current_process().name, len(fetched_posts)))
    return fetched_posts
  
  def parallel_fetch(self, verbose_mode=False, max_workers=None):
    """  Downloads posts in parallel processes.
    Each worker downloads independent segment. """

    from multiprocessing import cpu_count
    from concurrent.futures import ProcessPoolExecutor
    from concurrent.futures import as_completed

    # Total number of posts to download
    num_posts = self._number_of_posts()
    
    num_workers = max_workers or cpu_count()

    fetched_posts = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
      futures = []
      for offset, count in self._distribute_posts(num_posts, num_workers):
        futures.append(executor.submit(self.fetch, offset, count, verbose_mode))

      for future in as_completed(futures):
        try:
          fetched_posts.extend(future.result())
        except Exception as error:
          raise RuntimeError(error)

    return fetched_posts
  
  def _distribute_posts(self, total_posts, workers):
    """ Uniformly distributes posts for downloading between workers.
    Returns next start position for downloading and number of posts to fetch. """

    per_worker = total_posts // workers + total_posts % workers
    for offset in range(0, total_posts, per_worker):
      if (offset + per_worker) < total_posts:
        yield offset, per_worker
      else:
        yield offset, total_posts - offset


def main():
  args = vars(parse_args())

  if args['days']:
    if (args['from'] or args['to']):
      print('vktop: error: -d/--days option cannot be used with '
            '-f/--from or -t/--to options', file=sys.stderr)
      sys.exit(1)
    else:
      args['from'] = datetime.date.today() - timedelta(days=args['days'])

  try:
    page_id = get_page_id(args['url'])
  except (RuntimeError, requests.exceptions.ConnectionError) as error:
    print('{}: runtime error: {}'.format(sys.argv[0], error), file=sys.stderr)
    sys.exit(1)
  
  print('Downloading posts. This may take some time, be patient...')

  downloader = PostDownloader(page_id, args['from'], args['to'])

  try:
    if (sys.version_info > (3, 0)):
      posts = downloader.parallel_fetch(args['verbose'], args['workers'])
    else:
      # TODO:
      # Python 2.x does not support concurrent.futures out of the box,
      # therefore in Python 2.x using synchronous downloading
      if args['workers']:
        print('\033[93m'
              'WARNING: Python 2.x does not support parallel downloading!'
              '\033[0m')
      posts = downloader.fetch(verbose_mode=args['verbose'])
  except KeyboardInterrupt:
    msg = '{}: {}'.format(sys.argv[0], "Keyboard interrupt. Exiting...")
    print(msg, file=sys.stderr)
    sys.exit(1)
  except VKApiError as error:
    print('{}: vk api error: {}'.format(sys.argv[0], error), file=sys.stderr)
    sys.exit(1)
  except Exception as error:
    msg = '{}: catastrophic error: {}'.format(sys.argv[0], error)
    print(msg, file=sys.stderr)
    sys.exit(1)

  if args['verbose']:
    LOGGER.debug('Sorting {} posts'.format(len(posts)))

  if args['reposts']:
    posts = sorted(posts, key=lambda x: -x.reposts)
  else:
    posts = sorted(posts, key=lambda x: -x.likes)

  pretty_print(posts[:args['top']])

if __name__ == '__main__':
  main()