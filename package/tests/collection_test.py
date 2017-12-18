import unittest
from unittest.mock import MagicMock, Mock
from . import Collection, db, ValidationRepo

class TestCollectionMethods(unittest.TestCase):
  def setUp(self):
    self.collection = Collection()

  def tearDown(self):
    ValidationRepo._instance = None
    ValidationRepo._initiated = 0
    db.connection = None

  def test_search_one(self):
    class User(Collection): pass

    db.connection = Mock()
    cursor = db.connection.cursor()
    cursor.description = [("id","sdfj"), ("name", "sdfjk")]
    cursor.fetchone = MagicMock(return_value=(1, "John"))

    result = User().search_one("query placeholder", [], {})
    self.assertTrue(result.id == 1)
    self.assertTrue(result.name == "John")

  def test_search_all(self):
    db.connection = Mock()
    execute = Mock()
    fetchall = MagicMock(return_value=[])
    db.connection.cursor = MagicMock(return_value=type('Something', (), dict(description=[], execute=execute, fetchall=fetchall)))
    self.collection.get_result = MagicMock(return_value=None)
    self.collection.build_query = MagicMock(return_value=None)
    self.collection.search_all({}, {}, {})

    db.connection.cursor.assert_called()
    execute.assert_called()
    # self.collection.get_result.assert_called()

  def test_get_result(self):
    pass
    # class User(Collection): pass

    # db.connection = Mock()
    # cursor = db.connection.cursor()
    # cursor.description = [("id","sdfj"), ("name", "sdfjk")]
    # cursor.fetchall = MagicMock(return_value=[(1, "John"), (2, "Peter")])

    # result = User().get_result(cursor, ())
    # self.assertTrue(len(result) == 2)
    # self.assertTrue([isinstance(entry, User) for entry in result])

#   def test_build_assoc(self):
#     class GroupUser(Collection): pass
#     user = GroupUser()
#     case1 = {
#       "INNER JOIN": {
#         "user_posts": {
#           "type": "has_many",
#           "primary_key": "id",
#           "foreign_key": "group_user_id",
#           "primary_class": "GroupUser",
#           "foreign_class": "UserPost"
#         }
#       }
#     }
#     case2 = {
#       "INNER JOIN": {
#         "user_posts": {
#           "type": "has_many",
#           "primary_key": "id",
#           "foreign_key": "group_user_id",
#           "primary_class": "GroupUser",
#           "foreign_class": "UserPost"
#         },
#         "comments": {
#           "type": "has_many",
#           "primary_key": "id",
#           "foreign_key": "group_user_id",
#           "primary_class": "GroupUser",
#           "foreign_class": "Comments"
#         }
#       }
#     }

#     expected_result2 = """
# INNER JOIN user_posts AS user_posts
# ON group_users.id=user_posts.group_user_id
# INNER JOIN comments AS comments
# ON group_users.id=comments.group_user_id"""

#     expected_result1 = """
# INNER JOIN user_posts AS user_posts
# ON group_users.id=user_posts.group_user_id"""
#     self.assertTrue(user.build_assoc(case1) == expected_result1)
#     self.assertTrue(user.build_assoc(case2) == expected_result2)

  def test_build_conds(self):
    query1 = {"where": "a > 2"}
    query2 = {"within": "a in (2, 3, 4)"}
    query3 = {"where": "a > 2", "within": "a in (2, 3, 4)"}
    query4 = {"between": "a BETWEEN 1 and 5"}
    query5 = {"where": "a > 5", "between": "a BETWEEN 1 and 5"}

    expected_result1 = " WHERE a > 2"
    expected_result2 = " WHERE a in (2, 3, 4)"
    expected_result3 = " WHERE a > 2 AND a in (2, 3, 4)"
    expected_result4 = " WHERE a BETWEEN 1 and 5"
    expected_result5 = " WHERE a > 5 AND a BETWEEN 1 and 5"
    self.assertTrue(self.collection._Collection__build_conds(query1) == expected_result1)
    self.assertTrue(self.collection._Collection__build_conds(query2) == expected_result2)
    self.assertTrue(self.collection._Collection__build_conds(query3) == expected_result3)
    self.assertTrue(self.collection._Collection__build_conds(query4) == expected_result4)
    self.assertTrue(self.collection._Collection__build_conds(query5) == expected_result5)


  def test_build_sort(self):
    expected_result1 = " ORDER BY id"
    expected_result2 = " ORDER BY id LIMIT 5"
    expected_result3 = " ORDER BY id LIMIT 10 OFFSET 10"
    expected_result4 = " LIMIT 10 OFFSET 10"
    expected_result5 = " OFFSET 10"
    expected_result6 = ""

    self.assertTrue(self.collection._Collection__build_sort({"order": "id"}) == expected_result1)
    self.assertTrue(self.collection._Collection__build_sort({"order": "id", "limit": 5}) == expected_result2)
    self.assertTrue(self.collection._Collection__build_sort({"order": "id", "limit": 10, "offset": 10}) == expected_result3)
    self.assertTrue(self.collection._Collection__build_sort({"limit": 10, "offset": 10}) == expected_result4)
    self.assertTrue(self.collection._Collection__build_sort({"offset": 10}) == expected_result5)
    self.assertTrue(self.collection._Collection__build_sort({}) == expected_result6)
