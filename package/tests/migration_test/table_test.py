import unittest
from .. import Table
from unittest.mock import MagicMock, Mock
import re

class TestTable(unittest.TestCase):
  def test_getattr(self):
    m = MagicMock(return_value=None)
    __init__ = Table.__init__
    Table.__init__ = m
    Table.create("clubs")
    m.assert_called()
    m.assert_called_with("create", "clubs")
    m.reset_mock()
    Table.__init__ == __init__

  def test_getattr_validation(self):
    with self.assertRaises(AttributeError) as context:
      Table.random()
