##Dependencies
- [Requests] module (`pip install requests`)
- Python 3

##Help
```
usage: vktop.py [-h] [-l | -r] [-t TOP] [-d DAYS] url

Sort posts of any public availabe page at VK.com.
Github: https://github.com/yutkin/VK-Top

Possible types of input URLs:
- https://vk.com/page_name
- http://vk.com/club12345
- public1234567
- id1234567
- event1234567

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

[example]: http://s11.postimg.org/5xs9hakk3/Screen_Shot_2016_01_09_at_00_05_24.png "Example"
[Requests]: https://github.com/kennethreitz/requests
