import inflection

class Association:
  def __init__(self):
    self._associations = {}

  def __getattr__(self, name):
    return "Unrecognized association: {}".format(name)

  def has_many(self, assoc_table, **kwargs):
    class_name = inflection.singularize(assoc_table)
    table_name = inflection.underscore(assoc_table)
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = inflection.underscore(self.__class__.__name__) + "_id" if "foreign_key" not in kwargs else kwargs["foreign_key"]

    self._associations[table_name] = {
      "type": "has_many",
      "assoc_class": inflection.singularize(assoc_table),
      "primary_key": p_key,
      "foreign_key": f_key
    }

  def belongs_to(self, assoc_table, **kwargs):
    table_name = inflection.underscore(inflection.pluralize(assoc_table))
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = "{}_id".format(inflection.underscore(assoc_table)) if "foreign_key" not in kwargs else kwargs["foreign_key"]

    self._associations[table_name] = {
      "type": "belongs_to",
      "assoc_class": assoc_table,
      "primary_key": p_key,
      "foreign_key": f_key
    }

  def has_many_through(self, assoc_table, **kwargs):
    pass

  def include(self, class_name, **kwargs):
    # class_name UserPost
    # table_name user_posts
    table_name = inflection.pluralize(inflection.underscore(class_name))
    if table_name not in self._associations:
      logger.error("Assoication {} not defined".format(class_name))
      return

    return Relation(self.)

  def join(self):
    pass
