class Relation(object):
  def __init__(self, callback):
    self.callback = callback
    self.__conditions = {}
    self.__used_associations = []
    self.__collection = "all"
    self.results = []

  def __setitem__(self, *args):
    self.get_result()
    return self.callback(self.__collection, self.__conditions, self.__used_associations)

  def __getitem__(self, index):
    self.get_result()
    return self.results[index]

  def __delitem__(self, *args):
    self.get_result()
    return self.results

  def __getattr__(self, val):
    self.get_result()
    return self.results

  def get_result(self):
    if not self.results:
      self.results = self.callback(self.__collection, self.__conditions, self.__used_associations)

  def find(self):
    self.__collection = "find"
    return self

  def all(self):
    self.__collection = "all"
    return self

  def where(self, where_str):
    if "where" in self.__conditions:
      self.__conditions["where"] += " AND " + where_str
    else:
      self.__conditions["where"] = where_str

    return self

  def within(self, in_str):
    if "within" in self.__conditions:
      self.__conditions["within"] += " AND " + in_str
    else:
      self.__conditions["within"] = in_str
    return self

  def between(self, between):
    if "between" in self.__conditions:
      self.__conditions["between"] += " AND " + between
    else:
      self.__conditions["between"] = between
    return self

  def limit(self, limit):
    self.__conditions["limit"] = limit
    return self

  def select(self, select_str):
    if "select" in self.__conditions:
      self.__conditions["select"] += ", " + select_str
    else:
      self.__conditions["select"] = select_str
    return self

  def order(self, *order_str, **kwargs):
    order_clause = ""
    if kwargs:
      order_clauses = []
      for key, value in kwargs.items():
        order_clauses.append("{} {}".format(key, value))

      order_clause = (", ").join(order_clauses)

    if order_str:
      if len(order_clause) > 0:
        order_clause += ", " + order_str
      else:
        order_clause = (", ").join(list(order_str))

    if len(order_clause) > 0:
      if "order" in self.__conditions:
        self.__conditions["order"] += ", " + order_clause
      else:
        self.__conditions["order"] = order_clause

    return self

  def includes(self, tables):
    self.__used_associations.extend(tables)
    return self

  # def __add_join(self, join_type, tables):
  #   if join_type in self.__used_associations:
  #     self.__used_associations[join_type].append(tables)
  #   else:
  #     self.__used_associations[join_type] = tables

  # def join(self, tables):
  #   self.__add_join("INNER JOIN", tables)
  #   return self

  # def left_join(self, tables):
  #   self.__add_join("LEFT OUTER JOIN", tables)
  #   return self

  # def inner_join(self, tables):
  #   self.__add_join("INNER JOIN", tables)
  #   return self
