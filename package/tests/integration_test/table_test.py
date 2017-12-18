import unittest
from .. import Table, Column
import re

class TestTable(unittest.TestCase):

  def test_generate_command_create(self):
    t = Table("create", "groups", # id will be added unless
      title=Column.text(null=False, index=True, unique=True),
      id=Column.int()
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


  def test_generate_command_drop(self):
    t = Table("drop", "groups", cascade=True)

    command = t.generate_command()
    expected = """DROP TABLE groups CASCADE;"""
    self.assertEqual(re.sub(r"\s{2,}|\n|\t", '', command), re.sub(r"\s{2,}|\n|\t", '', expected))

  def test_generate_command_alter(self):
    column = Column.text()
    column.method = "alter"
    t = Table("alter", "groups",
      title=column
    )
    command = t.generate_command()
    expected = """ALTER TABLE groups ALTER COLUMN title TEXT;
    """
    self.assertEqual(re.sub(r"\s{2,}|\n|\t", '', command), re.sub(r"\s{2,}|\n|\t", '', expected))
