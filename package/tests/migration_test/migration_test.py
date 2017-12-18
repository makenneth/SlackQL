import unittest
from .. import Migration, Table, Column

class TestMigration(unittest.TestCase):
  def setUp(self):
    self.m = Migration()

  def test_create_table(self):
    return_value = self.m.create_table(
      "groups",
      title=Column.text(null=False, index=True, unique=True),
      id=Column.int()
    )

    self.assertTrue(isinstance(return_value, Table))
