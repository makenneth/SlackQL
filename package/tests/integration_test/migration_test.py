import unittest
from .. import Migration, Datatype
import re
class TestMigrationIntegration(unittest.TestCase):
  def setUp(self):
    self.m = Migration()

  def test_create_table(self):
    t = self.m.create_table("groups", # id will be added unless
      title=Datatype.text(null=False, index=True, unique=True),
      id=Datatype.int()
    )
    t.add_constraint(unique=("a", "c"), name="product_no")
    t.add_constraint(primary_key=("a", "c"), name="product_pk")
    t.add_constraint(name="fk_group", foreign_key=("group_id",), on_delete="cascade")

    command = self.m.migrations[0].generate_command()
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

  def test_parse_datatypes(self):
    t = Table("create", "posts")

    return_value = t.parse_datatypes(
      {
        "title": Column.text(null=False, index=True, unique=True),
        "cost": Column.int(null=False)
      }
    )
    indices = ["CREATE INDEX ON posts (title);"]
    fields = ["title TEXT NOT NULL UNIQUE", "cost INT NOT NULL"]
    self.assertEqual(len(return_value), 2)
    self.assertEqual(return_value[0], fields)
    self.assertEqual(return_value[1], indices)


