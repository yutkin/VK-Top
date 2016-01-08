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


import argparse
import const
from datetime import datetime, timedelta
import json
import sys
import requests
import time

class HiddenWall(BaseException):
    """ Dummy exception """
    pass


class PageNotAvailable(BaseException):
    """ Dummy exception """
    pass


def url_validator(arg):
    """ Checks correctness of url argument """
    arg = arg.lower()

    # If url something like https://vk.com/textual_id
    matched_txt_id = const.TXT_ID_REGEXP.match(arg)
    if matched_txt_id:
        url = matched_txt_id.groupdict()
        url['type'] = 'symbolic'
        return url

    # If url something like https://vk.com/id123456
    matched_numeric_id = const.NUM_ID_REGEXP.match(arg)
    if matched_numeric_id:
        return matched_numeric_id.groupdict()

    raise argparse.ArgumentTypeError(
            const.INVALID_URL.format(url=arg))


def num_validator(arg):
    """ Checks numbers on negativity """
    num = int(arg)
    if num >= 0:
        return num
    else:
        raise argparse.ArgumentTypeError(
                const.NEGATIVE_ARGUMENT.format(argument=arg))


def parse_args():
    """ Parses input arguments """
    parser = argparse.ArgumentParser(description=const.APP_DESCRIPTION,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('url',
                        action='store',
                        default=None,
                        help='target page',
                        type=url_validator)

    compar_key = parser.add_mutually_exclusive_group()

    compar_key.add_argument('-l',
                       '--likes',
                       help='sort posts by likes (by default)',
                       action='store_true',
                       default=True)

    compar_key.add_argument('-r',
                       '--reposts',
                       help='sort posts by reposts',
                       action='store_true')

    parser.add_argument('-t',
                        '--top',
                        help='number of showing posts. (10 by default)',
                        default=10,
                        type=num_validator)

    parser.add_argument('-d',
                        '--days',
                        type=int,
                        default=-1,
                        help='last period (in days) for post processing. '
                             '(all period by default)')

    return parser.parse_args()


def get_page_id(url):
    """ Returns page's numeric ID """
    if url['type'] not in ['id', 'public', 'event', 'club']:
        params = {'screen_name': url['id']}
        request = requests.get(const.API_URL + 'utils.resolveScreenName?',
                               params=params)
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


def recieve_posts(page_id, last_days, reposts):
    """
    Returns posts from :page_id: that were posted not earlier
    than :last_days: ago
    """
    deadline = datetime.now() - timedelta(days=last_days)
    unix_stamp = int(deadline.strftime("%s"))

    if reposts:
        compar_key = const.REPOSTS
    else:
        compar_key = const.LIKES

    params = {'access_token': const.ACCESS_TOKEN,
              'id': page_id,
              'compar_key': compar_key,
              'deadline':  unix_stamp if last_days != -1 else last_days
              }
    received_posts = []

    offset = 0
    ONGOING = True
    while ONGOING:
        params['offset'] = offset
        response = json.loads(requests.post(
            const.API_URL + 'execute.getPostsNew?', params=params).text)

        if 'error' in response:
            error = response['error']['error_code']
            if error == const.MANY_REQUESTS:
                continue
            if error == const.HIDDEN_WALL:
                raise HiddenWall('Wall is closed for outside view')
            raise RuntimeError(response['error']['error_msg'])

        # Interrupt loop when all posts were received
        if not response['response']:
            break

        received_data = response['response']
        for chunk in received_data:
            chunk_size = len(chunk['ids'])
            for i in range(chunk_size):
                post = dict()
                post['date'] = datetime.fromtimestamp(chunk['dates'][i])
                if chunk[compar_key][i] and (last_days == -1
                    or post['date'].year >= deadline.year
                    and post['date'].month >= deadline.month
                    and post['date'].day >= deadline.day):

                    post['id'] = chunk['ids'][i]
                    post[compar_key] = chunk[compar_key][i]
                    received_posts.append(post)
            if 'stop' in chunk:
                ONGOING = False
                break
        offset += 1

    return received_posts


def sort_posts(posts, reposts=False):
    """ Sort posts by specified parameter """
    if reposts:
        return sorted(posts, key=lambda post: -post['reposts'])
    else:
        return sorted(posts, key=lambda post: -post['likes'])


def main():
    """  Main entry point for execution as a program """

    init_point = time.time()
    args = parse_args()
    try:
        page_id = get_page_id(args.url)
        print('Downloading posts. '
              'This may take some time, be patient...')
        received_posts = recieve_posts(page_id, args.days, args.reposts)
        received_posts = sort_posts(received_posts, args.reposts)
    except (PageNotAvailable, HiddenWall) as error:
        print('{0}: error: {1}'.format(sys.argv[0], error))
        return
    except KeyboardInterrupt:
        print('Exiting...')
        return
    except Exception:
        print('{0}: error: {1}'.format(sys.argv[0], 'Unknown error'))
        return


    post_count = len(received_posts)
    if args.top and post_count:
        num_posts_for_showing = post_count if args.top > post_count else args.top
    elif post_count:
        num_posts_for_showing = post_count
    else:
        return

    max_url_width = len(str(max(received_posts, key=lambda x: x['id'])['id'])) + \
                    len('https://vk.com/wall_') + len(str(page_id))

    print('Elapsed time: {:.2f} sec.'.format(time.time() - init_point))
    for i, post in enumerate(received_posts[:num_posts_for_showing]):
        link = 'https://vk.com/wall{0}_{1}'.format(page_id, post['id'])
        print('{num:>{num_width}} {url:<{url_width}} {date:<14} {type}: {count:,}'.format(
            num=str(i+1)+')',
            num_width=len(str(num_posts_for_showing))+1,
            url=link,
            url_width=max_url_width + 4,
            date=str(post['date'])[:10],
            type='Reposts' if args.reposts else 'Likes',
            count=post['reposts'] if args.reposts else post['likes'])
        )

if __name__ == '__main__':
    main()
