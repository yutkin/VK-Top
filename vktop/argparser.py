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
import constants


def url_validator(arg):
  """ Check correctness of url argument """
  arg = arg.lower()
  
  # If url looks like http[s]://vk.com/domain
  symbolic_id = constants.TXT_ID_REGEXP.match(arg)
  if symbolic_id:
    url = symbolic_id.groupdict()
    url['type'] = 'domain'
    return url
  
  # If url looks like http[s]://vk.com/id123456
  numeric_id = constants.NUM_ID_REGEXP.match(arg)
  if numeric_id:
    url = numeric_id.groupdict()
    return url
  
  raise argparse.ArgumentTypeError(
    '{} - invalid url address'.format(arg))


def positiveness_validator(arg):
  """ Check number on positiveness """
  num = int(arg)
  if num > 0:
    return num
  else:
    raise argparse.ArgumentTypeError(
      '{} - must be a positive number'.format(arg))


def parse_args():
  """ Parses input arguments """
  parser = argparse.ArgumentParser(description=constants.APP_DESCRIPTION,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
  
  parser.add_argument('url',
                      action='store',
                      default=None,
                      help='target page',
                      type=url_validator)
  
  compar_key = parser.add_mutually_exclusive_group()
  
  compar_key.add_argument('-l',
                          '--likes',
                          help='sort by likes (default)',
                          action='store_true',
                          default=True)
  
  compar_key.add_argument('-r',
                          '--reposts',
                          help='sort by reposts',
                          action='store_true',
                          default=False)
  
  parser.add_argument('-t',
                      '--top',
                      help='# of posts to show (10 by default)',
                      default=10,
                      type=positiveness_validator)
  
  parser.add_argument('-w',
                      '--workers',
                      help='# of concurrent workers (# of CPU cores by default)',
                      default=None,
                      type=positiveness_validator)
  
  # parser.add_argument('-d',
  #   '--days',
  #   type=int,
  #   default=None,
  #   help='get the posts published only in the last -d days'
  #        '(from the beginning of time by default)')
  
  return parser.parse_args()
