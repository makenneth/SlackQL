import inflection
from . import repository

class Association:
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
