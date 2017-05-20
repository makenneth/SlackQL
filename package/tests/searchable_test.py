import unittest
from unittest.mock import MagicMock, Mock
from . import Searchable, Relation

class TestSearchableMethods(unittest.TestCase):
  def setUp(self):
    self.s = Searchable()
    self.s.apply_query = MagicMock()

  def test_find(self):
    self.s.find(5)
    self.s.apply_query.assert_called_with("one", { "where": "id = 5" }, [])

  def test_find_by(self):
    self.s.find_by(id=5, name=2)
    self.s.apply_query.assert_called_with("one", { "where": "id = 5 AND name = 2"}, [])

  def test_all(self):
    result = self.s.all()
    self.assertTrue(isinstance(result, Relation))

  def test_select(self):
    result = self.s.select("id", "name")
    self.assertTrue(isinstance(result, Relation))

  def test_where_not(self):
    pass

  def test_where(self):
    result = self.s.where(a=5, b= 6)
    self.assertTrue(isinstance(result, Relation))

  def test_within(self):
    result = self.s.within("a", [5, 6])
    self.assertTrue(isinstance(result, Relation))

  def test_between(self):
    result = self.s.between("a", 5, 6)
    self.assertTrue(isinstance(result, Relation))

  def test_limit(self):
    result = self.s.limit(5)
    self.assertTrue(isinstance(result, Relation))

  def test_order(self):
    result = self.s.order(name="DESC", age="ASC")
    self.assertTrue(isinstance(result, Relation))
