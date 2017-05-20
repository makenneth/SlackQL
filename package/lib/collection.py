import inflection
import numbers
from .relation import Relation
from .searchable import Searchable
from .validation import Validation
from .association import Association
from . import logger, db, repository, helpers
from time import time

class Collection(Searchable, Validation, Association):
  def columns(self):
    if db.connection:
      cursor = db.connection.cursor()
      # cache this
      if not self.__columns:
        cursor.execute("SELECT * FROM {} LIMIT 0".format(self.table_name()))
        self.__columns = [tuple[0] for tuple in cursor.description]
      return self.__columns

    return []

  def __init__(self, **kwargs):
    super(Collection, self).__init__()
    if self.set_validations:
      self.set_validations()
    if self.set_associations:
      self.set_associations()
    for column in self.columns():
      setattr(self, column, kwargs[column] if column in kwargs else None)

  def table_name(self, *args):
    if not self.__table:
      if args:
        self.__table = args[0]
      else:
        self.__table = inflection.underscore(inflection.pluralize(self.__class__.__name__))
    return self.__table

  def insert(self, **kwargs):
    values, columns = "", ""
    cursor = db.connection.cursor()
    for i, key in enumerate(kwargs):
      if not i == 0:
        columns += ", "
        values += ", "

      columns += key
      if isinstance(kwargs[key], numbers.Number):
        values += str(kwargs[key])
      else:
        values += "'" + kwargs[key] + "'"

    logger.info("Transaction begin:")
    start = time()
    sql_str = """\nINSERT INTO {table_name} ({columns}) VALUES ({values});""".format(
        table_name=self.table_name(),
        columns=columns,
        values=values
        )
    logger.info(sql_str)
    cursor.execute(sql_str)
    db.connection.commit()
    logger.info("Transaction Commited: {0:.2f}ms".format((time() - start) * 1000))
    self.id = cursor.lastrowid
    return True

  def update(self, **kwargs):
    cursor = db.connection.cursor()
    values = ""

    for i, key in enumerate(kwargs):
      if not i == 0:
        values += ", "

      values += "'{column}={value}'".format(column=key, value=kwargs[key])

    sql_str = """\nUPDATE {table_name} SET {queries}""".format(self.table_name(), values)
    logger.info("Transaction begin:")
    logger.info(sql_str)
    cursor.execute(sql_str)
    db.connection.commit()
    logger.info("Transaction Commited: {0:.2f}ms".format((time() - start) * 1000))

    return True

  def destroy(self, id):
    pass

  def save(self, **kwargs):
    attrs = {}
    for key, val in kwargs.items():
      if key in self.columns():
        setattr(self, key, val)

    if not self.validate():
      logger.warning("ROLLBACK Transaction.")
      return self

    for key, val in self:
      if val and key != "_associations":
        attrs[key] = val

    if "id" in attrs:
      return self.update(**attrs)
    else:
      return self.insert(**attrs)

  def apply_query(self, collection, *args):
    if collection == "all":
      return self.search_all(*args)
    else:
      return self.search_one(*args)

  def search_all(self, query, associations):
    query = self.build_query(query)
    cursor = db.connection.cursor()
    cursor.execute(query)
    return self.get_result(cursor, associations)

  def search_one(self, query, associations):
    cursor = db.connection.cursor()
    query = """
    SELECT {select_clause} FROM {table_name}{where_clause} LIMIT 1;""".format(
      select_clause=self.build_select(query),
      table_name=self.table_name(),
      where_clause=self.build_conds(query)
    )
    logger.info(query)
    cursor.execute(query)
    attr = {}
    columns = [tuple[0] for tuple in cursor.description]
    result = cursor.fetchone()
    if not result:
      logger.warning("No such entry found")
      return None
    else:
      for i in range(len(result)):
        attr[columns[i]] = result[i]

    return type(self.__class__.__name__, (), attr)

  def get_all_key_used(self, assoc_tables, associations):
    referenced_keys = {}
    associations = repository.Association.get_associations(self.__class__.__name__)
    for table in assoc_tables:
      assoc_class = helpers.class_to_table(table.__name__)
      association = associations[assoc_class]

      if association["type"] == "belongs_to":
        referenced_keys[association["foreign_key"]] = True
      elif association["type"] == "has_many":
        referenced_keys[association["primary_key"]] = True

    return referenced_keys

  def get_result(self, cursor, assoc_tables):
    associations = repository.Association.get_associations(self.__class__.__name__)
    self_class_name = self.__class__.__name__
    result, attr = [], {}
    result_key_reference = {}
    all_key_referenced = self.get_all_key_used(assoc_tables, associations)

    columns = [tuple[0] for tuple in cursor.description]
    for item in cursor.fetchall():
      for i in range(len(item)):
        attr[columns[i]] = item[i]

      new_entry = type(self_class_name, (), attr)
      for key in all_key_referenced:
        if not key in result_key_reference:
          result_key_reference[key] = {}

        result_key_reference[key][attr[key]] = new_entry
      result.append(new_entry)

    if len(assoc_tables) > 0:
      for table in assoc_tables:
        reference_key, reference_keys = None, []
        other_key, reference_class_name = None, None

        assoc_class = helpers.class_to_table(table.__name__)
        association = associations[assoc_class]
        if association["type"] == "has_many":
          reference_class_name = association["foreign_class"]
          reference_key = association["primary_key"]
          other_key = association["foreign_key"]
        elif association["type"] == "belongs_to":
          reference_class_name = association["primary_class"]
          reference_key = association["foreign_key"]
          other_key = association["foreign_key"]
        else:
          raise ValueError("Association not supported")

        reference_keys = [getattr(r, reference_key) for r in result]
        reference_class = type(reference_class_name, (Collection,), {})
        reference_results = reference_class().within(other_key, reference_keys)
        associated_result_dict = {}

        for item in reference_results:
          key = getattr(item, other_key)
          if not key in associated_result_dict:
            associated_result_dict[key] = []
          associated_result_dict[key].append(item)

        attr_name = inflection.pluralize(inflection.underscore(reference_class_name))
        for key, item in associated_result_dict.items():
          referenced_object = result_key_reference[reference_key][key]
          setattr(referenced_object, attr_name, item)

    return result

  def build_conds(self, query):
    query_str = ""
    if "where" in query:
      query_str += " WHERE {}".format(query["where"])
    if "within" in query:
      query_str += " WHERE " + query["within"] if query_str == "" else " AND " + query["within"]
    if "between" in query:
      query_str += " WHERE {}".format(query["between"]) if query_str == "" else " AND " + query["between"]
    return query_str

  def build_sort(self, query):
    query_str = ""
    if "order" in query:
      query_str += " ORDER BY {}".format(query["order"])
    if "limit" in query:
      query_str += " LIMIT {}".format(query["limit"])
    if "offset" in query:
      query_str += " OFFSET {}".format(query["offset"])

    return query_str

  def build_select(self, query):
    return query["select"] if "select" in query else "*"
  # def build_assoc(self, associations):
  #   assocs = ""

  #   added_associations = repository.Association.get_associations(self.__class__.__name__)
  #   if not added_associations:
  #     return assocs

  #   for join_type, tables in associations.items():
  #     # have to get associations here.. so the key for
  #     # the association repo should be different
  #     # should use something like table_name
  #     # so it can be quickly referenced

  #     for table_name in tables:
  #       if not table_name in added_associations:
  #         logger.error("Relationship {} not defined".format(table_name))
  #         continue
  #       rel = added_associations[table_name]
  #       assocs += """
  #   {join_type} {join_table_name} AS {join_table_name}
  #   ON {p_c}.{p_k}={f_c}.{f_k}""".format(
  #         join_type=join_type,
  #         join_table_name=table_name,
  #         p_c=self.class_to_table(rel["primary_class"]),
  #         f_c=self.class_to_table(rel["foreign_class"]),
  #         p_k=rel["primary_key"],
  #         f_k=rel["foreign_key"]
  #       )

  #   return assocs

  def build_query(self, query):
    # assocs = self.build_assoc(associations)
    # alias = self.table_name() if len(associations) > 0 else ""
    # alias_clause = " AS {}".format(self.table_name()) if alias != "" else ""
    # need to account for foreign table
    query_str = """
    SELECT {} FROM {}{}{};""".format(
      self.build_select(query),
      self.table_name(),
      self.build_conds(query),
      self.build_sort(query)
    )
    logger.info(query_str)
    return query_str

  def __iter__(self):
    for key, val in self.__dict__.items():
      if "__" not in key:
       yield key, val

  def __getattr__(self, val, *args, **kwargs):
    if val == "belongs_to" or val == "has_many":
      def wrapper(*args, **kwargs):
        getattr(repository.Association, val)(self.__class__.__name__, *args, **kwargs)
      return wrapper
    elif callable(val):
      print("Invalid method {}".format(val.__name__))
    else:
      return None
