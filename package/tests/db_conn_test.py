import unittest
import importlib
from unittest.mock import MagicMock, Mock
from . import DBConn

class TestDBConn(unittest.TestCase):
  def tearDown(self):
    DBConn.connection = None

  def test_configure(self):
    with self.assertRaises(ValueError) as context:
      DBConn.configure()

    with self.assertRaises(ValueError) as context:
      DBConn.configure(db_name="TestDB", database_engine="oracle")

    connect_mysql = DBConn.connect_mysql
    DBConn.connection = None
    DBConn.connect_mysql = Mock()
    DBConn.configure(db_name="TestDB", database_engine="mysql")
    DBConn.connect_mysql.assert_called()
    DBConn.connect_mysql = connect_mysql

    connect_psql = DBConn.connect_psql
    DBConn.connection = None
    DBConn.connect_psql = Mock()
    DBConn.configure(db_name="TestDB", database_engine="psql")
    DBConn.connect_psql.assert_called()
    DBConn.connect_psql = connect_psql

    connect_sqlite3 = DBConn.connect_sqlite3
    DBConn.connection = None
    DBConn.connect_sqlite3 = Mock()
    DBConn.configure(db_name="TestDB", database_engine="sqlite3")
    DBConn.connect_sqlite3.assert_called()
    DBConn.connect_sqlite3 = connect_sqlite3

  def test_connect_mysql(self):
    importlib.import_module = Mock()
    DBConn.connect_mysql(db_name="TestDB")
    importlib.import_module().connect.assert_called_with(
      port=3306,
      host="localhost",
      user="",
      passwd="",
      db="TestDB"
    )

  def test_connect_psql(self):
    importlib.import_module = Mock()
    DBConn.connect_psql(db_name="TestDB")
    importlib.import_module().connect.assert_called_with(
      port=5432,
      host="localhost",
      user="",
      password="",
      dbname="TestDB"
    )

  def test_connect_sqlite3(self):
    importlib.import_module = Mock()
    DBConn.connect_sqlite3(db_name="TestDB")
    importlib.import_module().connect.assert_called()
