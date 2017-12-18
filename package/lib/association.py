import inflection
from . import repository, helpers, Logger
from .slack_cache import Cache


class Association:
  def includes(self, *args):
    return Cache(self.apply_query).includes(*args)

  # def join(self, *args, **kwargs):
  #   table_names = []
  #   for join_class in args:
  #     table_name = None
  #     class_name = None
  #     if type(join_class) == str:
  #       class_name = join_class
  #       table_name = helpers.class_to_table(join_class)
  #     else:
  #       class_name = join_class.__name__
  #       table_name = helpers.class_to_table(class_name)
  #     if table_name not in repository.Association.get_associations(self.__class__.__name__):
  #       logger.error("Assoication {} not defined".format(class_name))
  #       return
  #     table_names.append(table_name)
  #   return Cache(self.apply_join).join(table_names)

  # def left_join(self):
  #   table_names = []
  #   for class_name in args:
  #     table_name = helpers.class_to_table(class_name)
  #     if table_name not in self._associations:
  #       logger.error("Assoication {} not defined".format(class_name))
  #       return

  #     table_names.append(table_name)

  #   return Cache(self.apply_join).left_join(table_names)

  # def inner_join(self):
  #   table_names = []
  #   for class_name in args:
  #     table_name = helpers.class_to_table(class_name)
  #     if table_name not in self._associations:
  #       logger.error("Assoication {} not defined".format(class_name))
  #       return

  #     table_names.append(table_name)

  #   return Cache(self.apply_join).inner_join(table_names)

  # def apply_join(self, cond, associations):
  #   return self.search_all(cond, associations)
