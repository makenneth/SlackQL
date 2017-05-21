from . import helpers

class Cache(object):
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

  def find(self, fid):
    return self.where(id=fid).find_one()

  def find_by(self, *args, **kwargs):
    return self.where(*args, **kwargs).find_one()

  def find_one(self):
    self.__collection = "one"
    return self.callback(self.__collection, self.__conditions, self.__used_associations)

  def all(self):
    self.__collection = "all"
    return self

  def where(self, *args, **kwargs):
    if len(args) == 0 and len(kwargs) == 0:
      logger.Info("Where requires at least one arguments. Call will be ignored.")
      return self

    where_clause = " AND ".join(args)
    for i, (key, val) in enumerate(kwargs.items()):
      if not where_clause == "":
        where_clause += " AND "
      where_clause += "{} = {}".format(
        key,
        helpers.format_clause_value(val)
      )

    if "where" in self.__conditions:
      self.__conditions["where"] += " AND " + where_clause
    else:
      self.__conditions["where"] = where_clause

    return self

  def within(self, *args, **kwargs):
    in_str = ""
    if len(args) > 1:
      within_values = (", ").join([helpers.format_clause_value(val) for val in args[1]])
      in_str = "{} {}IN ({})".format(
        args[0],
        "" if not kwargs or not kwargs["not"] else "{} ".format("NOT"),
        within_values
      )
    else:
      in_str = args[0]

    if "within" in self.__conditions:
      self.__conditions["within"] += " AND " + in_str
    else:
      self.__conditions["within"] = in_str

    return self

  def between(self, *args, **kwargs):
    if len(args) != 1 and len(args) != 3:
      logger.info("Between takes 1 or 3 arguemtns")
      return self

    between_clause = ""
    if len(args) == 3:
      between_clause = "{} {}BETWEEN {} AND {}".format(
        args[0],
        "" if not kwargs or not kwargs["not"] else "{} ".format("NOT"),
        helpers.format_clause_value(args[1]),
        helpers.format_clause_value(args[2])
      )
    else:
      between_clause = args[0]

    if "between" in self.__conditions:
      self.__conditions["between"] += " AND " + between_clause
    else:
      self.__conditions["between"] = between_clause
    return self

  def limit(self, limit):
    if type(limit) != int:
      logger.info("limit only takes integer as an argument")
      return self

    self.__conditions["limit"] = limit
    return self

  def select(self, *args):
    if len(args) == 0:
      logger.info("select requires at least one argument; call will be ignored")
      return self
    if "select" in self.__conditions:
      self.__conditions["select"] += ", " + (", ").join(args)
    else:
      self.__conditions["select"] = (", ").join(args)
    return self

  def order(self, *args, **kwargs):
    order_clause = ""
    if kwargs:
      order_clauses = []
      for key, value in kwargs.items():
        order_clauses.append("{} {}".format(key, value))

      order_clause = (", ").join(order_clauses)

    if args:
      if len(order_clause) > 0:
        order_clause += ", " + args
      else:
        order_clause = (", ").join(args)

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