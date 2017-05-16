import yaml, os
import importlib

SUPPORTED_ENGINE = {
  "mysql": "mysql",
  "psql": True,
  "sqlite3": True
}

DEFAULT_DATABASE_ENGINE = "sqlite3"
DEFAULT_PORTS = {
  "mysql": 3306,
  "psql": 5432
}
DEFAULT_HOST = "localhost"
DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = ""
DEFAULT_CONNECTION_TIMEOUT = ""
DEFAULT_DATABASE = "" # find it by path name

class Initialize:
  def read_config(self):
    script_dir = os.path.dirname(__file__)
    rel_path = "../config.yaml"
    abs_path = os.path.join(script_dir, rel_path)
    with open(abs_path, "r") as stream:
      return yaml.load(stream)

  def __init__(self):
    print("called")
    config = self.read_config()
    print(config)
    engine = "sqlite3"

    self.database = config["database"]
    if "database_engine" in config:
      if config["database_engine"] not in SUPPORTED_ENGINE:
        raise Exception

      engine = config["database_engine"]
    if engine != "sqlite3":
      self.port = config["port"] if "port" in config else DEFAULT_PORTS[engine]
      self.host = config["host"] if "host" in config else "localhost"
      self.username = config["username"] if "username" in config else ""
      self.password = config["password"] if "password" in config else ""
      self.connection_timeout = config["connection_timeout"] if "connection_timeout" in config else None

    getattr(self, "connect_{}".format(engine))()

  def connect_mysql(self):
    mysql = importlib.import_module("MySQLdb")
    connect_config = {
      "port": self.port,
      "host": self.host,
      "user": self.username,
      "passwd": self.password,
      "db": self.database
    }
    if self.connection_timeout:
      connect_config["connection_timeout"] = self.connection_timeout
    self.connection = mysql.connect(**connect_config)

  def connect_psql(self):
    psycopg2 = importlib.import_module("psycopg2")
    connect_config = {
      "port": self.port,
      "host": self.host,
      "user": self.username,
      "password": self.password,
      "dbname": self.database
    }
    if self.connection_timeout:
      connect_config["connection_timeout"] = self.connection_timeout
    self.connection = psycopg2.connect(**connect_config)

  def connect_sqlite3(self):
    sqlite3 = importlib.import_module("sqlite3")
    self.connection = sqlite3.connect(self.database)
