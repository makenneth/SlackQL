import sqlite3
from .relation import Relation
from .searchable import Searchable
from .validation import Validation
from . import logger
from time import time
class Collection(Searchable, Validation):
  def columns(self):
    if not self.__columns:
      self.__cursor.execute("SELECT * FROM {} LIMIT 0".format(self.__class__.__name__))
      self.__columns = [tuple[0] for tuple in self.__cursor.description]
    return self.__columns

  def __init__(self, **kwargs):
    super(Collection, self).__init__()
    self.set_validations()
    self.__connection = sqlite3.connect("twitter.db")
    self.__cursor = self.__connection.cursor()
    for column in self.columns():
      setattr(self, column, kwargs[column] if column in kwargs else None)

  def table_name(self, *args):
    if not self.__table:   
      if args:
        self.__table = args[0]
      else:
        self.__table = self.__class__.__name__

    return self.__table

  def insert(self, **kwargs):
    values, columns = "", ""

    for i, key in enumerate(kwargs):
      if not i == 0:
        columns += ", "
        values += ", "
      
      columns += "'" + key + "'"
      values += "'" + kwargs[key] + "'"
    logger.info("Transaction begin:")
    start = time()
    sql_str = """\nINSERT INTO {table_name} ({columns}) VALUES ({values});""".format(
        table_name=self.table_name(),
        columns=columns, 
        values=values
        )
    logger.info(sql_str)
    self.__cursor.execute(sql_str)
    self.__connection.commit()
    logger.info("Transaction Commited: {0:.2f}ms".format((time() - start) * 1000))
    self.__connection.close()
    self.id = self.__cursor.lastrowid
    return True

  def update(self, **kwargs):
    values = ""

    for i, key in enumerate(kwargs):
      if not i == 0:
        values += ", "

      values += "'{column}={value}'".format(column=key, value=kwargs[key]) 

    sql_str = """
      UPDATE {table_name} SET {queries}
    """.format(self.table_name(), values)
    logger.info(sql_str)
    self.__cursor.execute(sql_str)
    self.__connection.commit()
    self.__connection.close()

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
      if val:
        attrs[key] = val

    if "id" in attrs:
      return self.update(**attrs)
    else:
      return self.insert(**attrs)


  def search_all(self, query):
    self.__cursor.execute(self.build_query(query))
    return self.get_result()

  def search_one(self, query):
    self.__cursor.execute(query)
    attr = {}
    columns = [tuple[0] for tuple in self.__cursor.description]
    result = self.__cursor.fetchone()
    if not result:
      logger.warning("No such entry found")
      return None
    else:
      for i in range(len(result)):
        attr[columns[i]] = result[i] 

    return type(self.__class__.__name__, (), attr)

  def get_result(self):
    result, attr = [], {} 
    columns = [tuple[0] for tuple in self.__cursor.description]
    for item in self.__cursor.fetchall():
      for i in range(len(item)):
        attr[columns[i]] = item[i] 
      
      result.append(type(self.__class__.__name__, (), attr))

    return result

  def build_query(self, query):
    conditions = ""
    if "where" in query:
      conditions += " WHERE {}".format(query["where"])

    if "order" in query:
      conditions += " ORDER BY {}".format(query["order"])
    if "limit" in query:
      conditions += " LIMIT {}".format(query["limit"])
    query_str = """
      SELECT {} FROM {}{};
      """.format(query["select"] if "select" in query else "*", 
        self.table_name(), conditions)
    logger.info(query_str)
    return query_str

  def __iter__(self):
    for key, val in self.__dict__.items():
      if "__" not in key:
       yield key, val

  def __getattr__(self, val):
    if callable(val):
      print("Invalid method {}".format(val.__name__))
    else:
      return None
