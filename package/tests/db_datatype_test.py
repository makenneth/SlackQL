import unittest
from unittest.mock import MagicMock, Mock
import re
from . import Datatype

class TestDBDatatypes(unittest.TestCase):
  def test_get_index_with_bool(self):
    l = Datatype.get_index("users", "email", True)
    self.assertTrue(l == "CREATE INDEX ON users (email);")

  def test_get_index_with_dict(self):
    """ Test unique index """
    l1 = Datatype.get_index("users", "email", { "unique": True, "name": 'unique_email_idx' })
    cleaned1 = re.sub(r"\s{2,}|\n", '', l1)

    """ Test concurrently index """
    l2 = Datatype.get_index("users", "email", { "concurrently": True, "if_not_exists": True, "name": 'concurrent' })
    cleaned2 = re.sub(r"\s{2,}|\n", '', l2)

    """ Test method """
    l3 = Datatype.get_index("users", "email", { "name": "method_key", "using_method": "hash" })
    cleaned3 = re.sub(r"\s{2,}|\n", '', l3)

    self.assertEqual(cleaned1, "CREATE UNIQUE INDEX unique_email_idx ON users (email);")
    self.assertEqual(cleaned2, "CREATE INDEX CONCURRENTLY IF NOT EXISTS concurrent ON users (email);")
    self.assertEqual(cleaned3, "CREATE INDEX method_key ON users USING hash (email);")


  def test_get_column_clause(self):
    l1 = Datatype.get_column_clause("email", "text", {"unique": True, "null": False })
    l2 = Datatype.get_column_clause("age", "int", { "check": "age > 18", "null": False })
    l3 = Datatype.get_column_clause("club_id", "int", { "references": "clubs" })
    l4 = Datatype.get_column_clause("id", "serial", { "primary_key": True })
    l5 = Datatype.get_column_clause("is_admin", "bool", { "default": False })

    self.assertEqual(l1, "email TEXT UNIQUE NOT NULL")
    self.assertEqual(l2, "age INT CHECK (age > 18) NOT NULL")
    self.assertEqual(l3, "club_id INT REFERENCES clubs")
    self.assertEqual(l4, "id SERIAL PRIMARY KEY")
    self.assertEqual(l5, "is_admin BOOL DEFAULT false")

  def test_parse_datatype_options(self):
    returned_function = Datatype.parse_datatype_options("int", null=False)
    self.assertTrue(callable(returned_function))
    return_value = returned_function("users", "age")
    self.assertTrue(len(return_value) == 2)

  def test_getattr_call(self):
    cl = Datatype
    org = cl.parse_datatype_options
    cl.parse_datatype_options = Mock()
    cl.int(null=False)
    cl.parse_datatype_options.assert_called_with("int", null=False)
    cl.parse_datatype_options = org
