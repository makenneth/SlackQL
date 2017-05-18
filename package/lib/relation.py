class Relation(object):
  def __init__(self, callback):
    self.callback = callback
    self.__conditions = {}
    self.__used_associations = {}

  def __setitem__(self, *args):
    return self.callback(self.__conditions, self.__used_associations)

  def __getitem__(self, index):
    results = self.callback(self.__conditions, self.__used_associations)
    return results[index]

  def __delitem__(self, *args):
    return self.callback(self.__conditions, self.__used_associations)

  def __getattr__(self, val):
    return self.callback(self.__conditions, self.__used_associations)

  def all(self):
    return self

  def where(self, where_str):
    if "where" in self.__conditions:
      self.__conditions["where"] += " and " + where_str
    else:
      self.__conditions["where"] = where_str

    return self

  def limit(self, limit):
    self.__conditions["limit"] = limit
    return self

  def select(self, select_str):
    self.__conditions["select"] = select_str
    return self

  def order(self, *order_str, **kwargs):
    if kwargs:
      if "ASC" not in kwargs and "DESC" not in kwargs:
        print("Warning: it may not produce a desired outcome if you do not provide ASC or DESC as a key")
      for key, value in kwargs.items():
        if key == "ASC" or key == "DESC":
         order_str = ("{} {}".format(value, key),)

    if order_str or kwargs:
      if "order" in self.__conditions:
        self.__conditions["order"] += ", " + order_str[0]
      else:
        self.__conditions["order"] = order_str[0]

    return self

  def __add_join(self, join_type, tables):
    if join_type in self.__used_associations:
      self.__used_associations["join_type"].append(tables)
    else:
      self.__used_associations["join_type"] = tables

  def join(self, tables):
    self.__add_join("INNER JOIN", tables)
    return self

  def left_join(self, tables):
    self.__add_join("LEFT OUTER JOIN", tables)
    return self

  def inner_join(self, tables):
    self.__add_join("INNER JOIN", tables)
    return self