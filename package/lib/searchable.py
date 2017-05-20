from .relation import Relation
from . import helpers
from . import logger

class Searchable:
  def find(self, fid):
    return Relation(self.apply_query).where("id = {}".format(fid)).find_one()

  def find_by(self, **kwargs):
    query = "SELECT * FROM {} WHERE {} LIMIT 1"
    conditions = []
    for key, val in kwargs.items():
      conditions.append("{} = {}".format(
        key,
        helpers.format_clause_value(val)
      ))

    return Relation(self.apply_query).where(*conditions).find_one()

  def all(self):
    return Relation(self.apply_query).all()

  def select(self, *args):
    return Relation(self.apply_query).select(*args)

  def where_not(self, *args, **kwargs):
    pass

  def where(self, *args, **kwargs):
    return Relation(self.apply_query).where(*args, **kwargs)

  def within(self, *args, **kwargs):
    return Relation(self.apply_query).within(*args, **kwargs)

  def between(self, *args, **kwargs):
    return Relation(self.apply_query).between(*args, **kwargs)

  def limit(self, number):
    return Relation(self.apply_query).limit(number)

  def order(self, *args, **kwargs):
    return Relation(self.apply_query).order(*args, **kwargs)
