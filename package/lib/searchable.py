from .slack_cache import Cache
from . import helpers

class Searchable(object):
  def find(self, fid):
    return Cache(self.apply_query).find(fid)

  def find_by(self, *args, **kwargs):
    return Cache(self.apply_query).find_by(*args, **kwargs)

  def all(self):
    return Cache(self.apply_query).all()

  def select(self, *args):
    return Cache(self.apply_query).select(*args)

  def where_not(self, *args, **kwargs):
    return Cache(self.apply_query).where_not(*args, **kwargs)

  def where(self, *args, **kwargs):
    return Cache(self.apply_query).where(*args, **kwargs)

  def within(self, *args, **kwargs):
    return Cache(self.apply_query).within(*args, **kwargs)

  def not_within(self, *args):
    return Cache(self.apply_query).not_within(*args)

  def between(self, *args, **kwargs):
    return Cache(self.apply_query).between(*args)

  def not_between(self, *args, **kwargs):
    return Cache(self.apply_query).not_between(*args, **kwargs)

  def limit(self, number):
    return Cache(self.apply_query).limit(number)

  def order(self, *args, **kwargs):
    return Cache(self.apply_query).order(*args, **kwargs)
