import yaml
from importlib import import_module

SUPPORTED_ENGINE = {
  "mysql": "mysql"
  "psql": True
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

class SlackQL:
  def read_config(self):
    with open("../config.yaml", "r") as stream:
      return yaml.load(stream)

  def __init__(self, **kwargs):
    config = self.read_config()
    engine = "sqlite3"

    self.database = config["database"]
    if "database_engine" in config:
      if "database_engine" not in SUPPORTED_ENGINE:
        raise Exception

      engine = config["database_engine"]
    if engine != sqlite3:
      self.port = config["port"] if "port" in config else DEFAULT_PORTS[engine]
      self.host = config["host"] if "host" in config else "localhost"
      self.username = config["username"] if "username" in config else ""
      self.password = config["password"] if "password" in config else ""
      if "connection_timeout" in config:
        self.connection_timeout = config["connection_timeout"]

    getattr(self, "connect_{}".format(engine))()

  def connect_mysql:
    __import__("mysql.connector")
    connect_config = {
      "port": self.port,
      "host": self.host,
      "username": self.username,
      "password": self.password,
      "database": self.database
    }
    if self.connection_timeout:
      connect_config["connection_timeout"] = self.connection_timeout
    self.__connection = mysql.connector.connect(**connect_config)

  def connect_psql:
    __import__("psycopg2")
    connect_config = {
      "port": self.port,
      "host": self.host,
      "username": self.username,
      "password": self.password,
      "database": self.database
    }
    if self.connection_timeout:
      connect_config["connection_timeout"] = self.connection_timeout
    self.__connection = mysql.connector.connect(**connect_config)

  def connect_sqlite3:
    __import__("sqlite3")
    self.__connection = sqlite3.connect(self.database)

