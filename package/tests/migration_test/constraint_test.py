import unittest
from unittest.mock import MagicMock, Mock
from .. import Constraint

class TestConstraint(unittest.TestCase):
  def test_column_constraint_name_validation(self):
    with self.assertRaises(ValueError) as context:
      Constraint.column({ "ternary_key": ("id",) })

    Constraint.column({
      "check": "age > 5",
      "primary_key": True,
      "references": "groups",
      "unique": True,
      "default": 18,
      "null": False,
    })

  def test_column(self):
    self.assertEqual(Constraint.column({ "primary_key": True }), "PRIMARY KEY")
    self.assertEqual(Constraint.column({ "primary_key": False }), "")
    self.assertEqual(Constraint.column({ "check": "age > 5" }), "CHECK (age > 5)")
    self.assertEqual(Constraint.column({ "unique": True }), "UNIQUE")
    self.assertEqual(Constraint.column({ "unique": False }), "")
    self.assertEqual(Constraint.column({ "null": False }), "NOT NULL")
    self.assertEqual(Constraint.column({ "null": True }), "")
    self.assertEqual(Constraint.column({ "default": 18 }), "DEFAULT 18")
    self.assertEqual(Constraint.column({ "default": 18, "null": False }), "DEFAULT 18 NOT NULL")
    self.assertEqual(Constraint.column({ "references": "clubs" }), "REFERENCES clubs")
    self.assertEqual(Constraint.column({ "references": { "table": "clubs", "on_delete": "cascade" }}), "REFERENCES clubs ON DELETE CASCADE")
    self.assertEqual(Constraint.column({ "references": { "table": "clubs", "match": "partial", "on_delete": "restrict" }}), "REFERENCES clubs MATCH PARTIAL ON DELETE RESTRICT")

  def test_table(self):
    self.assertTrue(Constraint.table({ "primary_key": ("id",) }) == "PRIMARY KEY (id)")
    self.assertTrue(Constraint.table({ "name": "fk_group", "foreign_key": ("group_id",), "on_delete": "cascade" }) == "CONSTRAINT fk_group FOREIGN KEY (group_id) ON DELETE CASCADE")
    self.assertTrue(Constraint.table({ "unique": ("username", "email") }) == "UNIQUE (username, email)")
    self.assertTrue(Constraint.table({ "check": "age >= 18" }) == "CHECK (age >= 18)")

  def test_format_foreign_constraint(self):
    self.assertTrue(Constraint.table({ "name": "fk_group", "foreign_key": ("group_id",), "on_delete": "cascade" }) == "CONSTRAINT fk_group FOREIGN KEY (group_id) ON DELETE CASCADE")
    self.assertTrue(Constraint.table({ "foreign_key": ("group_id",) }) == "FOREIGN KEY (group_id)")

  def test_foreign_constraint_validation(self):
    with self.assertRaises(ValueError) as context:
      Constraint.format_foreign_constraint("abc", {"on_delete": "random"})

  def test_table_constraint_name_validation(self):
    with self.assertRaises(ValueError) as context:
      Constraint.table({ "ternary_key": ("id",) })
    Constraint.table({
      "name": "abc",
      "check": "age >= 18",
      "primary_key": ("id", ),
      "foreign_key": ("group_id", ),
      "unique": ("username",),
      "exclude": "",
      "deferrable": True,
      "initially": "deferred",
      "on_delete": "restrict"
    })
