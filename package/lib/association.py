import inflection

class Association:
  def __init__(self):
    self._associations = {}

  def __getattr__(self, name):
    return "Unrecognized association: {}".format(name)

  def class_to_table(self, class_name):
    return inflection.pluralize(inflection.underscore(class_name))

  def has_many(self, assoc_table, **kwargs):
    table_name = inflection.underscore(assoc_table)
    primary_class = self.__class__.__name__
    foreign_class = inflection.singularize(assoc_table) if "foreign_class" not in kwargs else kwargs["foreign_class"]
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = inflection.underscore(self.__class__.__name__) + "_id" if "foreign_key" not in kwargs else kwargs["foreign_key"]

    self._associations[table_name] = {
      "type": "has_many",
      "primary_class": primary_class,
      "foreign_class": foreign_class,
      "primary_key": p_key,
      "foreign_key": f_key
    }

  def belongs_to(self, assoc_table, **kwargs):
    table_name = inflection.underscore(inflection.pluralize(assoc_table))
    primary_class = assoc_table
    foreign_class = self.__class__.__name__ if "foreign_class" not in kwargs else kwargs["foreign_class"]
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = "{}_id".format(inflection.underscore(assoc_table)) if "foreign_key" not in kwargs else kwargs["foreign_key"]

    self._associations[table_name] = {
      "type": "belongs_to",
      "primary_class": primary_class,
      "foreign_class": foreign_class,
      "primary_key": p_key,
      "foreign_key": f_key
    }

  def has_many_through(self, assoc_table, **kwargs):
    pass

  def join(self, *args, **kwargs):
    table_names = []
    for class_name in args:
      table_name = self.class_to_table(class_name)
      if table_name not in self._associations:
        logger.error("Assoication {} not defined".format(class_name))
        return

      table_names.append(table_name)

    return Relation(self.apply_join).join(table_names)

  def left_join(self):
    table_names = []
    for class_name in args:
      table_name = self.class_to_table(class_name)
      if table_name not in self._associations:
        logger.error("Assoication {} not defined".format(class_name))
        return

      table_names.append(table_name)

    return Relation(self.apply_join).left_join(table_names)

  def inner_join(self):
    table_names = []
    for class_name in args:
      table_name = self.class_to_table(class_name)
      if table_name not in self._associations:
        logger.error("Assoication {} not defined".format(class_name))
        return

      table_names.append(table_name)

    return Relation(self.apply_join).inner_join(table_names)

  def apply_join(self, cond, associations):
    pass
