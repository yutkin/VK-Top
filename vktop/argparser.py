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
import textwrap
import datetime

from . import constants

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
    '{} - invalid url address. Check help (-h option).'.format(arg))


def positiveness_validator(arg):
  """ Check number on positiveness """
  num = int(arg)
  if num > 0:
    return num
  else:
    raise argparse.ArgumentTypeError(
      '{} - must be a positive number'.format(arg))

def date_validator(arg):
  try:
    date = datetime.datetime.strptime(arg.replace('.', '-'), '%d-%m-%Y').date()
  except Exception:
    raise argparse.ArgumentTypeError(
      '{} - invalid date format. Check help (-h option).'.format(arg))
  return date

def parse_args():
  """ Parses input arguments """

  app_description = textwrap.dedent('''
  VK-Top is used for getting popular posts of any public available page at VK.com
  Project repository: https://github.com/yutkin/VK-Top''')

  parser = argparse.ArgumentParser(prog='vktop',
                                   usage='vktop <url> [options]',
                                   description=app_description,
                                   formatter_class=argparse.RawTextHelpFormatter)

  url_param_description = textwrap.dedent('''\
  target page

  Possible variants of input:
  - https://vk.com/page_name,
  - http://vk.com/public12345
  - club1234567
  - id1234567
  - event1234567
  ''')
  parser.add_argument('url',
                      action='store',
                      default=None,
                      help=url_param_description,
                      type=url_validator)
  
  compar_key = parser.add_mutually_exclusive_group()
  
  compar_key.add_argument('-l',
                          '--likes',
                          help='sort posts by number of likes (default)',
                          action='store_true',
                          default=True)
  
  compar_key.add_argument('-r',
                          '--reposts',
                          help='sort posts by number of reposts',
                          action='store_true',
                          default=False)
  
  parser.add_argument('-n',
                      '--top',
                      help='number of posts to show (10 by default)',
                      default=10,
                      type=positiveness_validator)
  
  parser.add_argument('-w', '--workers',
                      help=textwrap.dedent('''\
                      number of concurrent workers (= available CPU cores by default)'
                      WARNING: Python 2.x does not support parallel downloading!'''),
                      default=None,
                      type=positiveness_validator)


  parser.add_argument('-f',
                      '--from',
                      action='store',
                      type=date_validator,
                      default=None,
                      help=textwrap.dedent('''\
                      posts published before this date will not be processed
                      (current date by default)'''),
                      )

  parser.add_argument('-t',
                      '--to',
                      action='store',
                      type=date_validator,
                      default=None,
                      help=textwrap.dedent('''\
                      posts published after this date will not be processed
                      (the beginning of time by default)''')
                      )
  return parser.parse_args()
