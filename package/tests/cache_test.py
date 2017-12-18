import unittest
from unittest.mock import MagicMock
from . import Cache

class TestCache(unittest.TestCase):
  def setUp(self):
    m = MagicMock()
    m.__self__ = MagicMock()
    self.rel = Cache(m)

  def test_find(self):
    return_value = self.rel.find_one()
    self.assertTrue(self.rel._Cache__collection == "one")
    self.assertFalse(isinstance(return_value, Cache))

  def test_all(self):
    return_value = self.rel.all()
    self.assertTrue(self.rel._Cache__collection == "all")
    self.assertTrue(isinstance(return_value, Cache))

  def test_where(self):
    return_value = self.rel.where("a = 5")

    self.assertTrue(self.rel._Cache__conditions["where"] == "a = 5")
    return_value = self.rel.where("b = 8")
    self.assertTrue(self.rel._Cache__conditions["where"] == "a = 5 AND b = 8")
    self.assertTrue(isinstance(return_value, Cache))

  def test_within(self):
    return_value = self.rel.within("a IN (1, 2, 3)")
    self.assertTrue(self.rel._Cache__conditions["within"] == "a IN (1, 2, 3)")
    return_value = self.rel.within("b IN (4, 5, 6)")
    self.assertTrue(self.rel._Cache__conditions["within"] == "a IN (1, 2, 3) AND b IN (4, 5, 6)")
    self.assertTrue(isinstance(return_value, Cache))
    self.setUp()
    return_value = self.rel.within("a", ["1", "2", 3])
    self.assertTrue(self.rel._Cache__conditions["within"] == "a IN ('1', '2', 3)")
    return_value = self.rel.within("b IN (4, 5, 6)")
    self.assertTrue(self.rel._Cache__conditions["within"] == "a IN ('1', '2', 3) AND b IN (4, 5, 6)")

  def test_between(self):
    return_value = self.rel.between("a BETWEEN 3 AND 5")

    self.assertTrue(self.rel._Cache__conditions["between"] == "a BETWEEN 3 AND 5")
    return_value = self.rel.between("b BETWEEN 5 AND 8")
    self.assertTrue(self.rel._Cache__conditions["between"] == "a BETWEEN 3 AND 5 AND b BETWEEN 5 AND 8")
    self.assertTrue(isinstance(return_value, Cache))

    self.setUp()
    self.rel.between("a", 1, 5)
    self.assertTrue(self.rel._Cache__conditions["between"] == "a BETWEEN 1 AND 5")
    self.rel.between("b", "a", "c")
    self.assertTrue(self.rel._Cache__conditions["between"] == "a BETWEEN 1 AND 5 AND b BETWEEN 'a' AND 'c'")

  def test_limit(self):
    return_value = self.rel.limit(5)
    self.assertTrue(self.rel._Cache__conditions["limit"] == 5)
    self.assertTrue(isinstance(return_value, Cache))

  def test_select(self):
    self.rel.select("id, name")
    self.assertTrue(self.rel._Cache__conditions["select"] == "id, name")
    self.rel.select("nickname, age")
    self.assertTrue(self.rel._Cache__conditions["select"] == "id, name, nickname, age")
    self.setUp()
    self.rel.select("id", "name")
    self.assertTrue(self.rel._Cache__conditions["select"] == "id, name")
    self.rel.select("nickname, age", "title")
    self.assertTrue(self.rel._Cache__conditions["select"] == "id, name, nickname, age, title")

  def test_order(self):
    self.rel.order(name="DESC")
    self.assertTrue(self.rel._Cache__conditions["order"] == "name DESC")
    self.rel.order(id="ASC")
    self.assertTrue(self.rel._Cache__conditions["order"] == "name DESC, id ASC")
    self.rel.order("nickname DESC")
    self.assertTrue(self.rel._Cache__conditions["order"] == "name DESC, id ASC, nickname DESC")
    self.setUp()
    self.rel.order("nickname DESC")
    self.assertTrue(self.rel._Cache__conditions["order"] == "nickname DESC")

  def test_includes(self):
    return_value = self.rel.includes("Post")
    self.assertTrue(self.rel._Cache__used_associations == ["Post"])
    return_value = self.rel.includes("User")
    self.assertTrue(self.rel._Cache__used_associations == ["Post", "User"])
    self.assertTrue(isinstance(return_value, Cache))
