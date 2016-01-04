##Dependencies
- [Requests] module (`pip install requests`)
- Python 3

##Help
```
python vktop.py --help
usage: vktop.py [-h] [-l | -r] [-t TOP] [-d DAYS] url

Script shows posts of any public availabe page at VK.com
Posts sorted by likes or reposts in the descending order.
Github: https://github.com/yutkin/VK-Top

Possible types of input URLs:
* https://vk.com/page_name
* http://vk.com/club12345
* public1234567
* id1234567
* event1234567

positional arguments:
  url                   target page

optional arguments:
  -h, --help            show this help message and exit
  -l, --likes           sort posts by likes (by default)
  -r, --reposts         sort posts by reposts
  -t TOP, --top TOP     number of showing posts. (10 by default)
  -d DAYS, --days DAYS  last period (in days) for post processing. (all period
                        by default)
```
##Usage example
![alt text][example]

[example]: http://s14.postimg.org/rzcisida9/Screen_Shot_2016_01_05_at_00_39_12.png "Example"
[Requests]: https://github.com/kennethreitz/requests
