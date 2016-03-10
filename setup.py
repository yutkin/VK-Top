from setuptools import setup
setup(
  name = 'vktop',
  packages = ['vktop'],
  version = '1.0',
  description = 'Sort posts of any page at VK.com',
  author = 'Dmitry Yutkin',
  author_email = 'yutkinn@gmail.com',
  url = 'https://github.com/yutkin/VK-Top',
  download_url = 'https://github.com/yutkin/VK-Top/tarball/v1.0',
  include_package_data=True,
  license='LICENSE.txt',
  keywords = ['vk.com', 'vk', 'downloader', 'posts', 'social', 'networks'],
  classifiers = [],
  entry_points=dict(
    console_scripts=[
      'vktop=vktop.vktop:main'
    ]
  ),
  install_requires=['requests'],
  platforms=['any'],
)
