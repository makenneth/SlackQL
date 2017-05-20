import inflection

class Association(object):
  _instance = None
  __associations = {}
  def __new__(cls, *args, **kwargs):
    return cls

  def __getattr__(cls, name):
    return "Unrecognized association: {}".format(name)

  @classmethod
  def get_associations(cls, callee_class):
    if callee_class in cls.__associations:
      return cls.__associations[callee_class]

    return {}

  @classmethod
  def class_to_table(cls, class_name):
    return inflection.pluralize(inflection.underscore(class_name))

  @classmethod
  def has_many(cls, callee, assoc_table, **kwargs):
    if callee in cls.__associations:
      return

    cls.__associations[callee] = {}
    table_name = inflection.underscore(assoc_table)
    primary_class = callee
    foreign_class = inflection.singularize(assoc_table) if "foreign_class" not in kwargs else kwargs["foreign_class"]
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = inflection.underscore(callee) + "_id" if "foreign_key" not in kwargs else kwargs["foreign_key"]

    cls.__associations[callee][table_name] = {
      "type": "has_many",
      "primary_class": primary_class,
      "foreign_class": foreign_class,
      "primary_key": p_key,
      "foreign_key": f_key
    }

  @classmethod
  def belongs_to(cls, callee, assoc_table, **kwargs):
    if callee in cls.__associations:
      return

    cls.__associations[callee] = {}
    table_name = inflection.underscore(inflection.pluralize(assoc_table))
    primary_class = assoc_table
    foreign_class = callee if "foreign_class" not in kwargs else kwargs["foreign_class"]
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = "{}_id".format(inflection.underscore(assoc_table)) if "foreign_key" not in kwargs else kwargs["foreign_key"]

    cls.__associations[callee][table_name] = {
      "type": "belongs_to",
      "primary_class": primary_class,
      "foreign_class": foreign_class,
      "primary_key": p_key,
      "foreign_key": f_key
    }

  @classmethod
  def has_many_through(cls, assoc_table, **kwargs):
    pass
