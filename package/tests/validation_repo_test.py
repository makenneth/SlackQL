import unittest
from . import ValidationRepo as Validation, ValidationError

class TestValidationRepositoryMethod(unittest.TestCase):
  def setUp(self):
    self.validations = Validation()

  def tearDown(self):
    Validation._instance = None
    Validation._initiated = 0

  def test_add_validations_without_args(self):
    """
      adding validations without args should raise an error
    """
    with self.assertRaises(ValidationError) as context:
      self.validations.add_validations("User")

    self.assertTrue('At least one field is required', str(context.exception.expression))

  def test_add_validations_without_kwags(self):
    """
      adding validations without kwags should raise an error
    """
    with self.assertRaises(ValidationError) as context:
      self.validations.add_validations("User", "title", "body")

    self.assertTrue('At least one condition is required', str(context.exception.expression))

  def test_correct_add_validations(self):
    """
      adding validations with proper arguments should not raise any errors
    """
    class User: pass
    u = User()
    setattr(u, "title", "test title")
    raised = False
    try:
      self.validations.add_validations(u, "title", presence=True)
    except:
      raised = True
    self.assertFalse(raised, "exception raised")

  def test_add_presence_validation(self):
    self.validations.add_validations("User", "title", presence=True)
    added_validations = self.validations.get_validations("User")
    self.assertTrue("title" in added_validations)
    self.assertTrue("presence" in added_validations["title"])

    # has to be boolean
    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("User", "title", presence="True")

  def test_add_uniqueness_validation(self):
    self.validations.add_validations("User", "title", uniqueness=True)
    added_validations = self.validations.get_validations("User")
    self.assertTrue("title" in added_validations)
    self.assertTrue("uniqueness" in added_validations["title"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("User", "title", uniqueness="True")

  def test_add_inclusion_validation(self):
    self.validations.add_validations("User", "number", inclusion=["one", "two", "three"])
    added_validations = self.validations.get_validations("User")
    self.assertTrue("number" in added_validations)
    self.assertTrue("inclusion" in added_validations["number"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("User", "number", inclusion="abc")

  def test_add_length_validation(self):
    self.validations.add_validations("User", "password", length={ max: 8, min: 6 })
    added_validations = self.validations.get_validations("User")
    self.assertTrue("password" in added_validations)
    self.assertTrue("length" in added_validations["password"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("User", "password", length=5)

  def test_add_range_validation(self):
    self.validations.add_validations("Votes", "count", range={ max: 20, min: 5 })
    added_validations = self.validations.get_validations("Votes")
    self.assertTrue("count" in added_validations)
    self.assertTrue("range" in added_validations["count"])

    with self.assertRaises(TypeError) as context:
      self.validations.add_validations("Votes", "password", range=5)

if __name__ == "__main__":
    unittest.main()
