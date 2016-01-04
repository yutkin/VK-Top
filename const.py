import re

ACCESS_TOKEN = 'fa32f7e88fc054f31a43e43cf4fa0109e7a4da7196e7e855bc1522e8fef8bda7c575eab6884d8e272d1a1a941ece3'

API_URL = 'https://api.vk.com/method/'
API_V = 5.37
TXT_ID_PTRN = r'(?:https?:\/\/)(?:vk.com\/(?!club|public|id|event))(?P<id>(?![_.])' \
              r'(?!club|public|id|event)[a-z0-9_.]*[a-z][a-z0-9_.]*)'

NUM_ID_PTRN = '^(?:https?:\/\/)?(?:vk.com\/)?(?P<type>club|public|id|event)' \
              '(?P<id>\d+)$'

TXT_ID_REGEXP = re.compile(TXT_ID_PTRN)
NUM_ID_REGEXP = re.compile(NUM_ID_PTRN)
