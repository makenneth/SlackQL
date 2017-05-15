import unittest, os, sys
from unittest.mock import MagicMock
sys.path.append(os.path.abspath(".."))
import SlackQL


class TestValidationsMethod(unittest.TestCase):
  def setUp(self):
    self.validations = SlackQL.Validation()

  def tearDown(self):
    pass

  def test_add_validations_without_args(self):
    """
      adding validations without args should raise an error
    """
    self.assertRaises(SlackQL.ValidationError, self.validations.add_validations)

  def test_add_validations_without_kwags(self):
    """
      adding validations without kwags should raise an error
    """
    with self.assertRaises(SlackQL.ValidationError) as context:
      self.validations.add_validations("title", "body")

    self.assertTrue('At least one condition is required', str(context.exception.expression))

  def test_correct_add_validations(self):
    """
      adding validations with proper arguments should not raise any errors
    """
    setattr(self.validations, "title", "test title")
    raised = False
    try:
      self.validations.add_validations("title", presence=True)
    except:
      raised = True
    self.assertFalse(raised, "exception raised")

  def test_add_presence_validation(self):
    setattr(self.validations, "title", "test title")
    self.validations.add_validations("title", presence=True)
    added_validations = self.validations.get_validations()
    self.assertTrue("title" in added_validations)
    self.assertTrue("presence" in added_validations["title"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("title", presence="True")

  def test_add_uniqueness_validation(self):
    setattr(self.validations, "title", "test title")
    self.validations.add_validations("title", uniqueness=True)
    added_validations = self.validations.get_validations()
    self.assertTrue("title" in added_validations)
    self.assertTrue("uniqueness" in added_validations["title"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("title", uniqueness="True")

  def test_add_inclusion_validation(self):
    setattr(self.validations, "number", "one")
    self.validations.add_validations("number", inclusion=["one", "two", "three"])
    added_validations = self.validations.get_validations()
    self.assertTrue("number" in added_validations)
    self.assertTrue("inclusion" in added_validations["number"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("number", inclusion="abc")

  def test_add_length_validation(self):
    setattr(self.validations, "password", "12345678")
    self.validations.add_validations("password", length={ max: 8, min: 6 })
    added_validations = self.validations.get_validations()
    self.assertTrue("password" in added_validations)
    self.assertTrue("length" in added_validations["password"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("password", length=5)

  def test_add_range_validation(self):
    setattr(self.validations, "count", "12345678")
    self.validations.add_validations("count", range={ max: 20, min: 5 })
    added_validations = self.validations.get_validations()
    self.assertTrue("count" in added_validations)
    self.assertTrue("range" in added_validations["count"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("password", range=5)

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

  def test_length_validation(self):
    setattr(self.validations, "password", "password")
    self.validations.add_validations("password", length={"min": 5, "max": 8})
    self.assertTrue(self.validations.validate())
    setattr(self.validations, "password", "pass")
    self.assertFalse(self.validations.validate())
    setattr(self.validations, "password", "passwords")
    self.assertFalse(self.validations.validate())

  def test_range_validation(self):
    setattr(self.validations, "count", 6)
    self.validations.add_validations("count", range={"min": 4, "max": 12})
    print(self.validations.get_validations())
    self.assertTrue(self.validations.validate())
    setattr(self.validations, "count", 2)
    self.assertFalse(self.validations.validate())
    setattr(self.validations, "count", 16)
    self.assertFalse(self.validations.validate())

if __name__ == "__main__":
    unittest.main()
