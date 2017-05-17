import inflection

class Association:
  _instance = None
  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(Association, cls).__new__(cls, *args, **kwargs)

    return cls._instance

  def __init__(self):
    self.__assocations = {}

  def __getattr__(self, name):
    return "Unrecognized association: {}".format(name)

  def get_associations(self):
    return self.__assocations

  def class_to_table(self, class_name):
    return inflection.pluralize(inflection.underscore(class_name))

  def has_many(self, callee, assoc_table, **kwargs):
    callee_class = callee.__class__.__name__
    if callee_class in self.__assocations:
      return

    self.__assocations[callee_class] = {}
    table_name = inflection.underscore(assoc_table)
    primary_class = callee_class
    foreign_class = inflection.singularize(assoc_table) if "foreign_class" not in kwargs else kwargs["foreign_class"]
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = inflection.underscore(callee_class) + "_id" if "foreign_key" not in kwargs else kwargs["foreign_key"]

    self.__assocations[callee_class][table_name] = {
      "type": "has_many",
      "primary_class": primary_class,
      "foreign_class": foreign_class,
      "primary_key": p_key,
      "foreign_key": f_key
    }

  def belongs_to(self, callee, assoc_table, **kwargs):
    callee_class = callee.__class__.__name__
    if callee_class in self.__assocations:
      return

    self.__assocations[callee_class] = {}
    table_name = inflection.underscore(inflection.pluralize(assoc_table))
    primary_class = assoc_table
    foreign_class = callee_class if "foreign_class" not in kwargs else kwargs["foreign_class"]
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = "{}_id".format(inflection.underscore(assoc_table)) if "foreign_key" not in kwargs else kwargs["foreign_key"]

    self.__assocations[table_name] = {
      "type": "belongs_to",
      "primary_class": primary_class,
      "foreign_class": foreign_class,
      "primary_key": p_key,
      "foreign_key": f_key
    }

  def has_many_through(self, assoc_table, **kwargs):
    pass
