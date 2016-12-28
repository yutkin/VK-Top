### Installation
`pip install vktop`

### Help
```
usage: vktop <url> [options]

VK-Top is used for getting popular posts of any public available page at VK.com
Project repository: https://github.com/yutkin/VK-Top

positional arguments:
  url                   target page

                        Possible variants of input:
                        - https://vk.com/page_name,
                        - http://vk.com/public12345
                        - club1234567
                        - id1234567
                        - event1234567

optional arguments:
  -h, --help            show this help message and exit
  -l, --likes           sort posts by number of likes (default)
  -r, --reposts         sort posts by number of reposts
  -t TOP, --top TOP     number of posts to show (10 by default)
  -w WORKERS, --workers WORKERS
                        number of concurrent workers (= available CPU cores by default)'
                        WARNING: Python 2.x does not support parallel downloading!
```
### Usage example
![alt text][example]

[example]: https://media.giphy.com/media/26FL98ClJbv6QzODu/source.gif "Example"
