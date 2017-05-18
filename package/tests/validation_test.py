import unittest
from unittest.mock import MagicMock
from . import Validation, ValidationRepo

class TestValidationMethods(unittest.TestCase):
  def setUp(self):
    self.validations = Validation()

  def tearDown(self):
    ValidationRepo._instance = None
    ValidationRepo._initiated = 0

  def test_presence_validation(self):
    setattr(self.validations, "title", "test title")
    self.validations.add_validations("title", presence=True)
    self.assertTrue(self.validations.validate())
    self.validations.add_validations("body", presence=True)
    self.assertFalse(self.validations.validate())

  def test_uniqueness_validation(self):
    setattr(self.validations, "username", "testuser1")
    self.validations.add_validations("username", uniqueness=True)
    self.validations.table_name = MagicMock(return_value="test")
    self.validations.search_one = MagicMock(return_value=False)
    self.assertTrue(self.validations.validate())
    setattr(self.validations, "username", "testuser2")
    self.validations.search_one = MagicMock(return_value=True)
    self.assertFalse(self.validations.validate())

  def test_inclusion_validation(self):
    setattr(self.validations, "number", "one")
    self.validations.add_validations("number", inclusion=["one", "two"])
    self.assertTrue(self.validations.validate())
    setattr(self.validations, "number", "three")
    self.assertFalse(self.validations.validate())

  def test_str_length_validation(self):
    setattr(self.validations, "password", "password")
    self.validations.add_validations("password", length={"min": 5, "max": 8})
    self.assertTrue(self.validations.validate())
    setattr(self.validations, "password", "pass")
    self.assertFalse(self.validations.validate())
    setattr(self.validations, "password", "passwords")
    self.assertFalse(self.validations.validate())

  def test_list_length_validation(self):
    setattr(self.validations, "tags", ["tag1", "tag2", "tag3"])
    self.validations.add_validations("tags", length={"min": 3, "max": 4})
    self.assertTrue(self.validations.validate())
    setattr(self.validations, "tags", ["tag1", "tag2"])
    self.assertFalse(self.validations.validate())
    setattr(self.validations, "tags", ["tag1", "tag2", "tag3", "tag4", "tag5"])
    self.assertFalse(self.validations.validate())

  def test_range_validation(self):
    setattr(self.validations, "count", 6)
    self.validations.add_validations("count", range={"min": 4, "max": 12})
    self.assertTrue(self.validations.validate())
    setattr(self.validations, "count", 2)
    self.assertFalse(self.validations.validate())
    setattr(self.validations, "count", 16)
    self.assertFalse(self.validations.validate())
