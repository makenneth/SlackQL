import unittest
from . import Table, Datatype
import re

class TestTable(unittest.TestCase):
  def test_generate_command(self):
    t = Table("groups", # id will be added unless
      title=Datatype.text(null=False, index=True, unique=True),
      id=Datatype.int()
    )
    t.add_constraint(unique=("a", "c"), name="product_no")
    t.add_constraint(primary_key=("a", "c"), name="product_pk")
    t.add_constraint(name="fk_group", foreign_key=("group_id",), on_delete="cascade")

    command = t.generate_command()
    expected = """
      CREATE TABLE groups (
        title TEXT NOT NULL UNIQUE,
        id INT,
        CONSTRAINT product_no UNIQUE (a, c),
        CONSTRAINT product_pk PRIMARY KEY (a, c),
        CONSTRAINT fk_group FOREIGN KEY (group_id) ON DELETE CASCADE
      );
    """
    self.assertEqual(re.sub(r"\s{2,}|\n|\t", '', command), re.sub(r"\s{2,}|\n|\t", '', expected))

  def test_add_constraint(self):
    t = Table("user")

    t.add_constraint(primary_key=("id",))
    t.add_constraint(name="fk_group", foreign_key=("group_id",), on_delete="cascade")
    t.add_constraint(unique=("username", "email"))
    t.add_constraint(check="age >= 18")
    self.assertTrue(t.constraints[0] == "PRIMARY KEY (id)")
    self.assertTrue(t.constraints[1] == "CONSTRAINT fk_group FOREIGN KEY (group_id) ON DELETE CASCADE")
    self.assertTrue(t.constraints[2] == "UNIQUE (username, email)")
    self.assertTrue(t.constraints[3] == "CHECK (age >= 18)")

  def test_parse_datatypes(self):
    t = Table("posts")

    return_value = t.parse_datatypes(
      "posts",
      {
        "title": Datatype.text(null=False, index=True, unique=True),
        "cost": Datatype.int(null=False)
      }
    )
    indices = ["CREATE INDEX ON posts (title);"]
    fields = ["title TEXT NOT NULL UNIQUE", "cost INT NOT NULL"]
    self.assertEqual(len(return_value), 2)
    self.assertEqual(return_value[0], fields)
    self.assertEqual(return_value[1], indices)
