import unittest
import importlib
from unittest.mock import MagicMock, Mock
from . import DBConn

class TestDBConn(unittest.TestCase):
  def tearDown(self):
    DBConn._instance = None

  def test_singleton(self):
    conn1 = DBConn()
    conn2 = DBConn()
    self.assertTrue(conn1 == conn2)

  def test_configure(self):
    conn = DBConn()
    with self.assertRaises(ValueError) as context:
      conn.configure()

    with self.assertRaises(ValueError) as context:
      conn.configure(db_name="TestDB", database_engine="oracle")

    conn.connect_mysql = Mock()
    conn.configure(db_name="TestDB", database_engine="mysql")
    conn.connect_mysql.assert_called()
    conn.connect_psql = Mock()
    conn.configure(db_name="TestDB", database_engine="psql")
    conn.connect_psql.assert_called()
    conn.connect_sqlite3 = Mock()
    conn.configure(db_name="TestDB", database_engine="sqlite3")
    conn.connect_sqlite3.assert_called()

  def test_connect_mysql(self):
    conn = DBConn()
    importlib.import_module = Mock()
    conn.connect_mysql(db_name="TestDB")
    importlib.import_module().connect.assert_called_with(
      port=3306,
      host="localhost",
      user="",
      passwd="",
      db="TestDB"
    )

  def test_connect_psql(self):
    conn = DBConn()
    importlib.import_module = Mock()
    conn.connect_psql(db_name="TestDB")
    importlib.import_module().connect.assert_called_with(
      port=5432,
      host="localhost",
      user="",
      password="",
      dbname="TestDB"
    )

  def test_connect_sqlite3(self):
    conn = DBConn()
    importlib.import_module = Mock()
    conn.connect_sqlite3(db_name="TestDB")
    importlib.import_module().connect.assert_called()
