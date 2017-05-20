import importlib

class DBConn:
  connection = None

  @classmethod
  def configure(cls, **kwargs):
    if not cls.connection:
      if "db_name" not in kwargs:
        raise ValueError("db_name must be present")

      db_name = kwargs["db_name"]
      if "database_engine" in kwargs:
        if kwargs["database_engine"] not in ["mysql", "psql", "sqlite3"]:
          raise ValueError("database engine not supported. Databases supported are: mysql, psql, and sqlite3 (default)")

      engine = kwargs["database_engine"]

      getattr(cls, "connect_{}".format(engine))(**kwargs)
    return cls.connection

  @classmethod
  def connect_mysql(cls, **kwargs):
    mysql = importlib.import_module("MySQLdb")
    connect_config = {
      "port": kwargs["port"] if "port" in kwargs else 3306,
      "host": kwargs["host"] if "host" in kwargs else "localhost",
      "user": kwargs["username"] if "user" in kwargs else "",
      "passwd": kwargs["password"] if "password" in kwargs else "",
      "db": kwargs["db_name"]
    }
    if "connection_timeout" in kwargs:
      connect_config["connection_timeout"] = kwargs["connection_timeout"]
    cls.connection = mysql.connect(**connect_config)

  @classmethod
  def connect_psql(cls, **kwargs):
    psycopg2 = importlib.import_module("psycopg2")
    connect_config = {
      "port": kwargs["port"] if "port" in kwargs else 5432,
      "host": kwargs["host"] if "host" in kwargs else "localhost",
      "user": kwargs["username"] if "user" in kwargs else "",
      "password": kwargs["password"] if "password" in kwargs else "",
      "dbname": kwargs["db_name"]
    }
    if "connection_timeout" in kwargs:
      connect_config["connection_timeout"] = kwargs["connection_timeout"]
    cls.connection = psycopg2.connect(**connect_config)

  @classmethod
  def connect_sqlite3(cls, **kwargs):
    sqlite3 = importlib.import_module("sqlite3")
    cls.connection = sqlite3.connect("{}.db".format(kwargs["db_name"]))

