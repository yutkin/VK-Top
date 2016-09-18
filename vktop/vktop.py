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
import sys
import argparser
import constants

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


class Post:
  def __init__(self, *, id, likes, reposts, date, text):
    self._id = id
    self._likes = likes
    self._reposts = reposts
    self._text = text
    self._date = date
  
  @property
  def id(self):
    return self._id

  @property
  def likes(self):
    return self._likes
  
  @property
  def reposts(self):
    return self._reposts
  
  @property
  def text(self):
    return self._text

  @property
  def date(self):
    return self._date

class PostsReceiver:
  def __init__(self, *, page_id):
    self.page_id = page_id
    self.api_url = constants.VKAPI_URL + 'wall.get'
    self.request_params = {'owner_id': self.page_id,
                           'v': constants.VKAPI_VERSION }
  
  def __number_of_posts(self):
    """ Returns total number of post on the page """
    self.request_params['offset'] = 0
    self.request_params['count'] = 1
    
    response = requests.get(self.api_url, params=self.request_params).json()
    
    if 'error' in response:
      raise VKApiError(response['error']['error_msg'])
    
    return response['response']['count']
  
  def receive(self, init_offset=None, num_posts=None):
    """ Synchronously downloads 'num_posts' posts starting
        from 'init_offset' position """
    
    if init_offset:
      self.request_params['offset'] = init_offset
    else:
      self.request_params['offset'] = 0
    if num_posts and num_posts < 100:
      self.request_params['count'] = num_posts
    else:
      self.request_params['count'] = 100
    
    
    posts = []
    total_received = 0
    while True:
      response = requests.get(self.api_url, params=self.request_params).json()
    
      if 'error' in response:
        raise VKApiError(response['error']['error_msg'])
      
      received_posts = response['response']['items']
      
      if not received_posts:
        break
      
      for post in received_posts:
        posts.append(Post(id=post['id'],
                          text=post['text'],
                          likes=post['likes']['count'],
                          reposts=post['reposts']['count'],
                          date=post['date']
                          ))
      total_received += len(received_posts)
  
      if total_received == num_posts:
        break
      
      self.request_params['offset'] += 100
      
      if num_posts:
        diff = abs(num_posts - total_received)
        self.request_params['count'] = 100 if diff > 100 else diff

    return posts
  
  def parallel_receive(self, *, max_workers=None):
    """  Downloads posts in parallel processes.
    Every worker process independent segment. """
    
    from multiprocessing import cpu_count
    from concurrent.futures import ProcessPoolExecutor
    from concurrent.futures import as_completed
    
    total_posts = self.__number_of_posts()
    
    workers = max_workers if max_workers else cpu_count()

    posts = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
      futures = [executor.submit(self.receive, offset, count)
                 for offset, count in self._distribute_posts(total_posts, workers)]

      for future in as_completed(futures):
        try:
          posts.extend(future.result())
        except Exception as exc:
          raise RuntimeError(exc)

    return posts
  
  def _distribute_posts(self, total_posts, workers):
    """ Returns next start position for downloading and number
     of posts to download. """
    per_worker = total_posts // workers + total_posts % workers
    for offset in range(0, total_posts, per_worker):
      if (offset + per_worker) < total_posts:
        yield offset, per_worker
      else:
        yield offset, total_posts - offset
      

def pretty_print(posts, page_id, by_reposts):
  """ Prints results in a pretty table """
  for i, post in enumerate(posts):
    post_link = 'https://vk.com/wall{0}_{1}'.format(page_id, post.id)
    print('{:<3} {:<50} {}: {}'.format(
      str(i+1)+'.',
      post_link,
      'Reposts' if by_reposts else 'Likes',
      post.reposts if by_reposts else post.likes))


def main():
  args = argparser.parse_args()

  try:
    page_id = get_page_id(args.url)
    
  except (RuntimeError, requests.exceptions.ConnectionError) as error:
    print('{}: runtime error: {}'.format(sys.argv[0], error), file=sys.stderr)
    sys.exit(1)
  
  print('Downloading posts. This may take some time, be patient...')

  postsReceiver = PostsReceiver(page_id=page_id)
  try:
    if not args.workers or args.workers > 1:
      posts = postsReceiver.parallel_receive(max_workers=args.workers)
    else:
      posts = postsReceiver.receive()
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
  
  if args.reposts:
    posts = sorted(posts, key=lambda x: -x.reposts)
  else:
    posts = sorted(posts, key=lambda x: -x.likes)

  pretty_print(posts[:args.top], page_id, args.reposts)

if __name__ == '__main__':
  main()