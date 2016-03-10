"""
This module defines the global constants.
"""

import re
import textwrap


APP_DESCRIPTION = textwrap.dedent('''
    Sort posts of any public availabe page at VK.com.
    Github: https://github.com/yutkin/VK-Top

    Possible types of input URLs:
    - https://vk.com/page_name
    - http://vk.com/club12345
    - public1234567
    - id1234567
    - event1234567
    ''')

LIKES = 'likes'
REPOSTS = 'reposts'

ACCESS_TOKEN = 'ff8faef07fe2666af8743cd4384fa595f85927d6c39dc4360e831a149d9f956710be447816dd857d2dee7'

API_URL = 'https://api.vk.com/method/'
API_V = 5.37

INVALID_URL = ('{url} - invalid url address')
NEGATIVE_ARGUMENT = ('{argument} - should be greater or equal to 0')
MANY_REQUESTS = 6
HIDDEN_WALL = 13


TXT_ID_PTRN = r'(?:https?:\/\/)(?:vk.com\/(?!club|public|id|event))(?P<id>(?![_.])(?!club|public|id|event)[a-z0-9_.]*[a-z][a-z0-9_.]*)'
NUM_ID_PTRN = r'^(?:https?:\/\/)?(?:vk.com\/)?(?P<type>club|public|id|event)(?P<id>\d+)$'
TXT_ID_REGEXP = re.compile(TXT_ID_PTRN)
NUM_ID_REGEXP = re.compile(NUM_ID_PTRN)
