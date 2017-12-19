import unittest
from unittest.mock import MagicMock, Mock
import re
from .. import Column, Datatype

class TestColumn(unittest.TestCase):
  def test_get_index_with_bool(self):
    l = Column("int", {}).get_index("users", "email", True)
    self.assertTrue(l == "CREATE INDEX ON users (email);")

  def test_set_method(self):
    l = Column("int", {})
    self.assertEqual(l.method, None)
    l.set_method("create")
    self.assertEqual(l.method, "create")

  def test_get_index_with_dict(self):
    """ Test unique index """
    l1 = Column("varchar", {}).get_index("users", "email", { "unique": True, "name": 'unique_email_idx' })
    cleaned1 = re.sub(r"\s{2,}|\n", '', l1)

    """ Test concurrently index """
    l2 = Column("varchar", {}).get_index("users", "email", { "concurrently": True, "if_not_exists": True, "name": 'concurrent' })
    cleaned2 = re.sub(r"\s{2,}|\n", '', l2)

    """ Test method """
    l3 = Column("varchar", {}).get_index("users", "email", { "name": "method_key", "using_method": "hash" })
    cleaned3 = re.sub(r"\s{2,}|\n", '', l3)

    self.assertEqual(cleaned1, "CREATE UNIQUE INDEX unique_email_idx ON users (email);")
    self.assertEqual(cleaned2, "CREATE INDEX CONCURRENTLY IF NOT EXISTS concurrent ON users (email);")
    self.assertEqual(cleaned3, "CREATE INDEX method_key ON users USING hash (email);")


  def test_get_column_clause(self):
    l1 = Column({ "unique": True, "null": False }, Datatype("text")).get_column_clause("email")
    l2 = Column({ "check": "age > 18", "null": False }, Datatype("int")).get_column_clause("age")
    l3 = Column({ "references": "clubs" }, Datatype("int")).get_column_clause("club_id")
    l4 = Column({ "primary_key": True }, Datatype("serial")).get_column_clause("id")
    l5 = Column({ "default": False }, Datatype("bool")).get_column_clause("is_admin")

    self.assertEqual(l1, "email TEXT UNIQUE NOT NULL")
    self.assertEqual(l2, "age INT CHECK (age > 18) NOT NULL")
    self.assertEqual(l3, "club_id INT REFERENCES clubs")
    self.assertEqual(l4, "id SERIAL PRIMARY KEY")
    self.assertEqual(l5, "is_admin BOOL DEFAULT false")

  def test_getattr_char(self):
    cl = Column.char(40)
    self.assertTrue(callable(cl))
    cl = cl(unique=True)
    self.assertTrue(type(cl) == Column)

  def test_getattr_set(self):
    cl = Column.set(null=False)
    self.assertTrue(type(cl) == Column)
    self.assertTrue(cl.method == "set")

  def test_getattr_char_length_test(self):
    with self.assertRaises(TypeError) as context:
      Column.varchar()

  def test_generate_command_rename(self):
    c = Column({"new_name": "body"}, None, "rename")
    command, = c.generate_command("post", "title")
    self.assertEqual(command, "RENAME COLUMN title TO body")

  def test_generate_command_set(self):
    c = Column({"default": None}, None, "set")
    command, = c.generate_command("post", "title")
    self.assertEqual(command, "ALTER COLUMN title DROP DEFAULT")
    # this might be an error... should be 'abc'?
    c = Column({"default": "abc"}, None, "set")
    command, = c.generate_command("post", "title")
    self.assertEqual(command, "ALTER COLUMN title SET DEFAULT \"abc\"")
    c = Column({"null": True}, None, "set")
    command, = c.generate_command("post", "title")
    self.assertEqual(command, "ALTER COLUMN title DROP NOT NULL")
    c = Column({"null": False}, None, "set")
    command, = c.generate_command("post", "title")
    self.assertEqual(command, "ALTER COLUMN title SET NOT NULL")

  def test_generate_command_drop(self):
    c = Column({"if_exists": True, "on_delete": "cascade"}, None, "drop")
    command, = c.generate_command("post", "title")
    self.assertEqual(command, "DROP COLUMN IF EXISTS title ON DELETE CASCADE")

  def test_generate_command_set_validations(self):
    c = Column({"not_supported_string": None}, None, "set")
    with self.assertRaises(ValueError) as context:
      command, = c.generate_command("post", "title")

