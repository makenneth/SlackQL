import unittest
from unittest.mock import MagicMock
from . import Relation

class TestRelation(unittest.TestCase):
  def setUp(self):
    self.rel = Relation(MagicMock())

  def test_find(self):
    return_value = self.rel.find()
    self.assertTrue(self.rel._Relation__collection != "all")
    self.assertTrue(isinstance(return_value, Relation))

  def test_all(self):
    return_value = self.rel.all()
    self.assertTrue(self.rel._Relation__collection == "all")
    self.assertTrue(isinstance(return_value, Relation))

  def test_where(self):
    return_value = self.rel.where("a = 5")

    self.assertTrue(self.rel._Relation__conditions["where"] == "a = 5")
    return_value = self.rel.where("b = 8")
    self.assertTrue(self.rel._Relation__conditions["where"] == "a = 5 AND b = 8")
    self.assertTrue(isinstance(return_value, Relation))

  def test_within(self):
    return_value = self.rel.within("a IN (1, 2, 3)")

    self.assertTrue(self.rel._Relation__conditions["within"] == "a IN (1, 2, 3)")
    return_value = self.rel.within("b IN (4, 5, 6)")
    self.assertTrue(self.rel._Relation__conditions["within"] == "a IN (1, 2, 3) AND b IN (4, 5, 6)")
    self.assertTrue(isinstance(return_value, Relation))

  def test_between(self):
    return_value = self.rel.between("a BETWEEN 3 AND 5")

    self.assertTrue(self.rel._Relation__conditions["between"] == "a BETWEEN 3 AND 5")
    return_value = self.rel.between("b BETWEEN 5 AND 8")
    self.assertTrue(self.rel._Relation__conditions["between"] == "a BETWEEN 3 AND 5 AND b BETWEEN 5 AND 8")
    self.assertTrue(isinstance(return_value, Relation))

  def test_limit(self):
    return_value = self.rel.limit(5)
    self.assertTrue(self.rel._Relation__conditions["limit"] == 5)
    self.assertTrue(isinstance(return_value, Relation))

  def test_select(self):
    self.rel.select("id, name")
    self.assertTrue(self.rel._Relation__conditions["select"] == "id, name")
    self.rel.select("nickname, age")
    self.assertTrue(self.rel._Relation__conditions["select"] == "id, name, nickname, age")

  def test_order(self):
    self.rel.order(name="DESC")
    self.assertTrue(self.rel._Relation__conditions["order"] == "name DESC")
    self.rel.order(id="ASC")
    self.assertTrue(self.rel._Relation__conditions["order"] == "name DESC, id ASC")
    self.rel.order("nickname DESC")
    self.assertTrue(self.rel._Relation__conditions["order"] == "name DESC, id ASC, nickname DESC")
    self.rel = Relation(MagicMock())
    self.rel.order("nickname DESC")
    self.assertTrue(self.rel._Relation__conditions["order"] == "nickname DESC")

  def test_includes(self):
    return_value = self.rel.includes(["Tweet", "Post"])
    self.assertTrue(self.rel._Relation__used_associations == ["Tweet", "Post"])
    return_value = self.rel.includes(["User"])
    self.assertTrue(self.rel._Relation__used_associations == ["Tweet", "Post", "User"])
    self.assertTrue(isinstance(return_value, Relation))
