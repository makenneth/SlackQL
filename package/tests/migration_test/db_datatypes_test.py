import unittest
from unittest.mock import MagicMock, Mock
from .. import Datatype

class TestDatatype(unittest.TestCase):
  def test_init(self):
    # __init__ should trigger verify_type
    orig = Datatype.verify_type
    m = Mock()
    Datatype.verify_type = m
    d = Datatype("int")
    m.assert_called_with("int")
    m.reset_mock()
    Datatype.verify_type = orig

  def test_to_str(self):
    # to_str should return the correct string representation of the datatype
    self.assertEqual(Datatype("int").to_str(), "INT")
    self.assertEqual(Datatype("text").to_str(), "TEXT")

    self.assertEqual(Datatype("varchar", length=30).to_str(), "VARCHAR(30)")

  def test_verify_type(self):
    # verify type should correctly catch invalid data type
    with self.assertRaises(AttributeError) as context:
      Datatype("string").verify_type()


