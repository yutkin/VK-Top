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

def pretty_print(posts, sorted_by_reposts, col_indent_len=10):
  """ Prints results as a pretty table """

  longest_url_len = max([len(post.url) for post in posts])
  longest_likes_len = max([len(str(post.likes)) for post in posts])
  longest_reposts_len = max([len(str(post.reposts)) for post in posts])

  for i, post in enumerate(posts):
    data = {
      'ind': str(i+1) + '.',
      'url': post.url,
      'likes': post.likes,
      'reposts': post.reposts,
      'url_len': longest_url_len + col_indent_len,
      'likes_len': longest_likes_len + col_indent_len,
      'reposts_len': longest_reposts_len + col_indent_len,
    }
    if sorted_by_reposts:
      print('{ind:<3} {url:<{url_len}} reposts {reposts:<{reposts_len}}'
            'likes: {likes:<{likes_len}} '.format(**data))
    else:
      print('{ind:<3} {url:<{url_len}} likes: {likes:<{likes_len}}'
            'reposts {reposts:<{reposts_len}}'.format(**data))
