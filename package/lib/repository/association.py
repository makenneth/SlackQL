import inflection
from .. import helpers

class Association(object):
  _instance = None
  __associations = {}
  def __new__(cls, *args, **kwargs):
    return cls

  @classmethod
  def get_associations(cls, callee_class):
    if callee_class in cls.__associations:
      return cls.__associations[callee_class]

    return {}

  @classmethod
  def has_many(cls, callee, assoc_table, **kwargs):
    relation_name = inflection.underscore(assoc_table)
    if callee in cls.__associations and relation_name in cls.__associations[callee]:
      return

    if not callee in cls.__associations:
      cls.__associations[callee] = {}

    if "through" in kwargs:
      cls.__associations[callee][relation_name] = {
        "type": "has_many_through",
        "source": kwargs["source"],
        "relation": kwargs["through"],
        "relation_names": [kwargs["through"], inflection.singularize(kwargs["through"])]
      }

    else:
      primary_class = callee
      foreign_class = inflection.titleize(inflection.singularize(assoc_table)) if "foreign_class" not in kwargs else kwargs["foreign_class"]
      p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
      f_key = inflection.underscore(callee) + "_id" if "foreign_key" not in kwargs else kwargs["foreign_key"]

      cls.__associations[callee][relation_name] = {
        "type": "has_many",
        "primary_class": primary_class,
        "foreign_class": foreign_class,
        "primary_key": p_key,
        "foreign_key": f_key
      }

  @classmethod
  def belongs_to(cls, callee, assoc_table, **kwargs):
    relation_name = helpers.class_to_table(assoc_table)
    if callee in cls.__associations and relation_name in cls.__associations[callee]:
      return

    cls.__associations[callee] = {}
    primary_class = inflection.titleize(assoc_table)
    foreign_class = callee if "foreign_class" not in kwargs else kwargs["foreign_class"]
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = "{}_id".format(inflection.underscore(assoc_table)) if "foreign_key" not in kwargs else kwargs["foreign_key"]

    cls.__associations[callee][relation_name] = {
      "type": "belongs_to",
      "primary_class": primary_class,
      "foreign_class": foreign_class,
      "primary_key": p_key,
      "foreign_key": f_key
    }
