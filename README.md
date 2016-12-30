### Installation
`pip install vktop`

### Help
```
usage: vktop <url> [options]

VK-Top is used for getting popular posts of any public available page at VK.com
Project repository: https://github.com/yutkin/VK-Top

Parameters:
  url                   target page

                        Possible variants of <url>:
                        - https://vk.com/page_name,
                        - http://vk.com/public12345
                        - club1234567
                        - id1234567
                        - event1234567

Options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l, --likes           sort posts by number of likes (default)
  -r, --reposts         sort posts by number of reposts
  -n <number>, --top <number>
                        number of posts to show
  -w <number>, --workers <number>
                        number of concurrent workers
                        WARNING: Python 2.x does not support parallel
                        downloading!
  -f <date>, --from <date>
                        discard posts published before this date
  -t <date>, --to <date>
                        discard posts published after this date
  --verbose             print debug messages
```
### Usage example
![alt text][example]

[example]: https://media.giphy.com/media/26FKTawVSwKO4ZHfq/source.gif "Example"
