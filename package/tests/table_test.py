import unittest
from . import Table, DBDatatypes

class TestTable(unittest.TestCase):
  def test_generate_command(self):
    # t = Table("group",
    #   id=data_type.int(primary=True, on_delete="cascade"),
    #   title=data_type.string(null=False, index=True, unique=True)
    # )
    # command = t.test_generate_command
    # should_be = ["""CREATE TABLES group (
    #   id serial PRIMARY KEY,
    #   title STRING NOT NULL UNIQUE
    # );"""]
    # self.assertTrue()
    pass

  def test_add_constraint(self):
    t = Table("user")

    t.add_constraint(primary_key=("id",))
    t.add_constraint(name="fk_group", foreign_key=("group_id",), on_delete="cascade")
    t.add_constraint(unique=("username", "email"))
    t.add_constraint(check="age >= 18")
    self.assertTrue(t.constraints[0] == "PRIMARY KEY (id)")
    self.assertTrue(t.constraints[1] == "CONSTRAINTS fk_group FOREIGN KEY (group_id) ON DELETE CASCADE")
    self.assertTrue(t.constraints[2] == "UNIQUE (username, email)")
    self.assertTrue(t.constraints[3] == "CHECK (age >= 18)")

  def test_parse_datatypes(self):
    t = Table("posts")

    return_value = t.parse_datatypes(
      "posts",
      {
        "title": DBDatatypes.text(null=False, index=True, unique=True),
        "cost": DBDatatypes.int(null=False)
      }
    )
    indices = ["CREATE INDEX ON posts (title);"]
    fields = ["title TEXT NOT NULL UNIQUE", "cost INT NOT NULL"]
    self.assertEqual(len(return_value), 2)
    self.assertEqual(return_value[0], fields)
    self.assertEqual(return_value[1], indices)
