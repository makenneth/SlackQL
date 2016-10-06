class Relation(object):
  def __init__(self, callback):
    self.callback = callback
    self.condition = {}

  def __setitem__(self, *args):
    return self.callback(self.condition)

  def __getitem__(self, index):
    results = self.callback(self.condition)
    return results[index]

  def __delitem__(self, *args):
    return self.callback(self.condition)

  def __getattr__(self, val):
    return self.callback(self.condition)

  def all(self):
    return self

  def where(self, where_str):
    if "where" in self.condition:
      self.condition["where"] += " and " + where_str
    else:
      self.condition["where"] = where_str

    return self

  def limit(self, limit):
    self.condition["limit"] = limit
    return self

  def select(self, select_str):
    self.condition["select"] = select_str
    return self

  def order(self, *order_str, **kwargs):
    if kwargs:
      if "ASC" not in kwargs and "DESC" not in kwargs:
        print("Warning: it may not product desired outcome if you do not provide ASC or DESC as a key")
      for key, value in kwargs.items():
        if key == "ASC" or key == "DESC":
         order_str = ("{} {}".format(value, key),)
    
    if order_str or kwargs:
      if "order" in self.condition:
        self.condition["order"] += ", " + order_str[0]
      else:
        self.condition["order"] = order_str[0]

    return self