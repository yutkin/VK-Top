class Post:
  def __init__(self, id, likes, reposts, date, text, url=None):
    self._id = id
    self._likes = likes
    self._reposts = reposts
    self._text = text
    self._date = date
    self._url = url

  @property
  def id(self):
    return self._id

  @property
  def likes(self):
    return self._likes

  @property
  def reposts(self):
    return self._reposts

  @property
  def text(self):
    return self._text

  @property
  def date(self):
    return self._date

  @property
  def url(self):
    return self._url