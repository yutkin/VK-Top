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

from setuptools import setup
from vktop import __version__ as app_version

setup(
  name = 'vktop',
  packages=['vktop'],
  install_requires=['requests'],
  version = app_version,
  description = 'VK-Top is used for getting popular posts of any public available page at VK.com',
  author = 'Dmitry Yutkin',
  author_email = 'yutkinn@gmail.com',
  url = 'https://github.com/yutkin/VK-Top',
  download_url = 'https://github.com/yutkin/VK-Top/tarball/'+app_version,
  include_package_data=True,
  license='MIT',
  keywords = ['vk.com', 'vk', 'downloader', 'posts', 'social', 'networks', 'likes', 'reposts'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS',
    'Operating System :: Unix',
    'Operating System :: Microsoft',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2',
    'Topic :: Internet',
    'Topic :: Utilities'
  ],
  entry_points=dict(
    console_scripts=[
        'vktop=vktop.__main__:main'
    ]
  ),
)
