import importlib

class DBConn:
  _instance = None
  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(DBConn, cls).__new__(cls, *args, **kwargs)

    return cls._instance

  def __init__(self):
    self.connection = None

  def configure(self, **kwargs):
    if "db_name" not in kwargs:
      raise ValueError("db_name must be present")

    db_name = kwargs["db_name"]
    if "database_engine" in kwargs:
      if kwargs["database_engine"] not in ["mysql", "psql", "sqlite3"]:
        raise ValueError("database engine not supported. Databases supported are: mysql, psql, and sqlite3 (default)")

    engine = kwargs["database_engine"]

    getattr(self, "connect_{}".format(engine))(**kwargs)

  def connect_mysql(self, **kwargs):
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
    self.connection = mysql.connect(**connect_config)

  def connect_psql(self, **kwargs):
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
    self.connection = psycopg2.connect(**connect_config)

  def connect_sqlite3(self, **kwargs):
    sqlite3 = importlib.import_module("sqlite3")
    self.connection = sqlite3.connect("{}.db".format(kwargs["db_name"]))

