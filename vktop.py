import json
import sys
from datetime import datetime, timedelta

import requests
import argparser

import const

class HiddenWall(Exception):
    """ Dummy exception """
    pass

class PageNotAvailable(Exception):
    """ Dummy exception """
    pass

def get_page_id(url):
    """
    Returns page numeric ID.

    If url looks like https://vk.com/id12345 than return 12345,
    else if url looks like https://vk.com/textual_name then
    makes request to VK and gets numeric id from response.

    """
    if url['type'] not in ['id', 'public', 'event', 'club']:
        params = {'screen_name': url['id']}
        request = requests.get(const.API_URL + 'utils.resolveScreenName?', params=params)
        response = json.loads(request.text)['response']

        if response:
            if response['type'] == 'user':
                return response['object_id']
            else:
                return -response['object_id']
        else:
            raise PageNotAvailable(url['id'] + ' is not available')
    elif url['type'] == 'id':
        return int(url['id'])
    else:
        return -int(url['id'])


def recieve_posts(page_id, last_days):
    """
    Returns :received_posts: from :page_id: that were posted not earlier than
    "today - :last_days:".

    In endless loop make response. If response without errors (contains posts)
    then in loop check received posts. If i-th post has appropriate date then
    add it into :received_posts:.

    """
    received_posts = []
    deadline = datetime.now() - timedelta(days=last_days)
    params = {'access_token': const.ACCESS_TOKEN, 'id': page_id}

    offset = 0
    while True:
        params['offset'] = offset
        response = json.loads(requests.post(
            const.API_URL + 'execute.getPosts?', params=params).text)


        if 'error' in response:
            # if many requests per second
            if response['error']['error_code'] == 6:
                continue
            # page has hidden wall
            elif response['error']['error_code'] == 13:
                raise HiddenWall('Wall is closed for outside view')
            else:
                raise RuntimeError

        # if received all posts from page
        if not response['response']:
            break

        received_data = response['response']
        for chunk in received_data:
            for i in range(chunk['chunk_size']):
                post = {}
                post['date'] = datetime.fromtimestamp(chunk['dates'][i])

                if last_days == -1 or post['date'].year >= deadline.year and \
                                post['date'].month >= deadline.month and \
                                post['date'].day >= deadline.day:
                    post['id'] = chunk['ids'][i]
                    post['likes'] = chunk['likes'][i]
                    post['reposts'] = chunk['reposts'][i]

                    if post['likes'] != None and post['reposts'] != None:
                        received_posts.append(post)
        offset += 1

    return received_posts

def sort_posts(posts, reposts=False):
    """ Sort posts by specified parameter. """
    if reposts:
        return sorted(posts, key=lambda post: -post['reposts'])
    else:
        return sorted(posts, key=lambda post: -post['likes'])

def main():
    args = argparser.parse_args()
    try:
        page_id = get_page_id(args.url)
        received_posts = sort_posts(recieve_posts(page_id, args.days), args.reposts)
    except (PageNotAvailable, HiddenWall) as error:
        print('{0}: error: {1}'.format(sys.argv[0], error))
        return
    except Exception:
        print('{0}: error: {1}'.format(sys.argv[0], 'Unknown error'))
        return

    post_count = len(received_posts)
    if args.top and post_count:
        num_posts_for_showing = post_count-1 if args.top > post_count else args.top
    elif post_count:
        num_posts_for_showing = post_count
    else:
        return

    max_url_width = len(str(max(received_posts, key=lambda x: x['id'])['id'])) + \
                    len('https://vk.com/wall_') + len(str(page_id))

    for i, post in enumerate(received_posts[:num_posts_for_showing]):
        link = 'https://vk.com/wall{0}_{1}'.format(page_id, post['id'])
        print('{num:>{num_width}} {url:<{url_width}} {date:<14} {type}: {count:,}'.format(
            num=str(i+1)+')',
            num_width=len(str(num_posts_for_showing))+1,
            url=link,
            url_width=max_url_width + 4,
            date=str(post['date'])[:10],
            type='Reposts' if args.reposts else 'Likes',
            count=post['reposts'] if args.reposts else post['likes'],
        ))

if __name__ == '__main__':
    main()
