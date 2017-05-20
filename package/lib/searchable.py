from .relation import Relation
from . import helpers
from . import logger

class Searchable:
  def find(self, fid):
    return self.search_one("""SELECT * FROM {} WHERE id = {}
      """.format(self.table_name(), fid))

  def find_by(self, **kwargs):
    query = "SELECT * FROM {} WHERE {} LIMIT 1"
    conditions = []
    for key, val in kwargs.items():
      conditions.append("{} = {}".format(
        key,
        helpers.format_clause_value(val)
      ))

    query = query.format(self.table_name(), " and ".join(conditions))

    return self.search_one(query)

  def all(self):
    return Relation(self.apply_query).all()

  def select(self, *args):
    if len(args) == 0:
      select_str = "*"
    else:
      select_str = ", ".join(args)

    return Relation(self.apply_query).select(select_str)

  def where(self, *args, **kwargs):
    where_str = ""
    if args != ():
      where_str = " and ".join(args)

    for i, (key, val) in enumerate(kwargs.items()):
      if not i == 0:
        where_str += " and "
      # account for numbers and date
      where_str += "{} = {}".format(
        key,
        helpers.format_clause_value(val)
      )

    return Relation(self.apply_query).where(where_str)

  def not_between(self, *args):
    pass

  def within(self, *args):
    if len(args) == 2:
      if type(args[1]) == list and type(args[0]) == str:
        within_str = "{} IN ({})".format(
          args[0],
          (", ").join([helpers.format_clause_value(val) for val in args[1]])
        )
        return Relation(self.apply_query).within(within_str)
    elif len(args) == 1 and type(args[0]) == str:
      return Relation(self.apply_query).within(args)

    return Relation(self.apply_query)

  def between(self, *args):
    if len(args) == 1:
      return Relation(self.apply_query).between(args)
    elif len(args) == 2:
      between_values = [helpers.format_clause_value(val) for val in args]
      return Relation(self.apply_query).between("BETWEEN" + " and ".join(args))

  def limit(self, number):
    if isinstance(number, int):
      return Relation(self.apply_query).limit(number)
    else:
      raise ValueError("Argument passed into limit must be an int")

  def order(self, **kwargs):
    order_str = None
    for key, value in kwargs.items():
      if key == "ASC" or key == "DESC":
       order_str = "{} {}".format(value, key)

    return Relation(self.apply_query).order(order_str)
