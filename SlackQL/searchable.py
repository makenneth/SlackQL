from .relation import Relation
class Searchable:
  def find(self, fid):
    return self.search_one("""SELECT * FROM {} WHERE id = {}
      """.format(self.table_name(), fid))

  def find_by(self, **kwargs):
    query = "SELECT * FROM {} WHERE {} LIMIT 1"
    conditions = []
    for key, val in kwargs.items():
      conditions.append("{} = '{}'".format(key, val))

    query = query.format(self.table_name(), " and ".join(conditions))
    
    return self.search_one(query)

  def all(self):
    return Relation(self.search_all).all()

  def select(self, *args):
    if len(args) == 0:
      select_str = "*"
    else:
      select_str = ", ".join(args)

    return Relation(self.search_all).select(select_str)

  def where(self, **kwargs):
    where_str = ""
    if isinstance(kwargs, str):
      where_str = kwargs
    else:
      for i, (key, val) in enumerate(kwargs.list()):
        if not i == 0:
          where_str += " and "
        where_str += "{} = {}".format(key, val)

    return Relation(self.search_all).where(where_str)

  def limit(self, number):
    if isinstance(number, int):
      return Relation(self.search_all).limit(number)
    else:
      raise ValueError("Argument passed into limit must be an int")

  def order(self, **kwargs):
    if "ASC" not in kwargs and "DESC" not in kwargs:
      print("Warning: it may not product desired outcome if you do not provide ASC or DESC as a key")
    order_str = None
    for key, value in kwargs.items():
      if key == "ASC" or key == "DESC":
       order_str = "{} {}".format(value, key)

    return Relation(self.search_all).order(order_str)

