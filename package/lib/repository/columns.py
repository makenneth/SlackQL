from .. import db

class Columns:
  _columns = {}

  @classmethod
  def get_columns(cls, table_name):
    if table_name not in cls._columns:
      columns = Columns.__query_columns(table_name)
      cls._columns[table_name] = columns

    return cls._columns[table_name]

  @classmethod
  def __query_columns(cls, table_name):
    if db.connection:
      cursor = db.connection.cursor()
      cursor.execute("SELECT * FROM {} LIMIT 0".format(table_name))
      return [tuple[0] for tuple in cursor.description]

    return []
