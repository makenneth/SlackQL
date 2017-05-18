import inflection
import numbers
from .relation import Relation
from .searchable import Searchable
from .validation import Validation
from .association import Association
from . import logger, db, repository
from time import time

class Collection(Searchable, Validation, Association):
  def columns(self):
    if db.connection:
      cursor = db.connection.cursor()
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

  def class_to_table(self, class_name):
    return inflection.pluralize(inflection.underscore(class_name))

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


  def search_all(self, query):
    db.connection.cursor().execute(self.build_query(query))
    return self.get_result()

  def search_one(self, query):
    cursor = db.connection.cursor()
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

  def get_result(self):
    cursor = db.connection.cursor()
    result, attr = [], {}
    columns = [tuple[0] for tuple in cursor.description]
    for item in cursor.fetchall():
      for i in range(len(item)):
        attr[columns[i]] = item[i]

      result.append(type(self.__class__.__name__, (), attr))

    return result

  def build_conds(self, query):
    query_str = ""
    # need to account for foreign table
    if "where" in query:
      query_str += " WHERE {}".format(query["where"])

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

  def build_assoc(self, associations):
    assocs = ""

    for join_type, tables in associations.items():
      for table_name, rel in tables.items():
        assocs += """
{join_type} {join_table_name} AS {join_table_name}
ON {p_c}.{p_k}={f_c}.{f_k}""".format(
          join_type=join_type,
          join_table_name=table_name,
          p_c=self.class_to_table(rel["primary_class"]),
          f_c=self.class_to_table(rel["foreign_class"]),
          p_k=rel["primary_key"],
          f_k=rel["foreign_key"]
        )

    return assocs

  def build_query(self, query, associations):
    conditions = self.build_conds(query)
    sort = self.build_sort(query)
    assocs = self.build_assoc(associations)
    alias = self.table_name() if len(associations) > 0 else ""
    alias_clause = " AS {}".format(self.table_name()[0]) if alias != "" else ""
    # need to account for foreign table
    query_str = """SELECT {} FROM {}{}{}{};""".format(
      query["select"] if "select" in query else "*",
      self.table_name(),
      alias,
      conditions,
      assocs,
      sort
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
        getattr(repository.Association(), val)(self.__class__.__name__, *args, **kwargs)
      return wrapper
    elif callable(val):
      print("Invalid method {}".format(val.__name__))
    else:
      return None
