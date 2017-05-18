import unittest
from . import Collection

class TestCollectionMethods(unittest.TestCase):
  def setUp(self):
    self.collection = Collection()

  def test_build_assoc(self):
    class GroupUser(Collection): pass
    class Comments(Collection): pass
    user_post = Comments()
    user = GroupUser()
    case1 = {
      "INNER JOIN": {
        "user_posts": {
          "type": "has_many",
          "primary_key": "id",
          "foreign_key": "group_user_id",
          "primary_class": "GroupUser",
          "foreign_class": "UserPost"
        }
      }
    }
    case2 = {
      "INNER JOIN": {
        "user_posts": {
          "type": "has_many",
          "primary_key": "id",
          "foreign_key": "group_user_id",
          "primary_class": "GroupUser",
          "foreign_class": "UserPost"
        },
        "comments": {
          "type": "has_many",
          "primary_key": "id",
          "foreign_key": "group_user_id",
          "primary_class": "GroupUser",
          "foreign_class": "Comments"
        }
      }
    }

    expected_result2 = """
INNER JOIN user_posts AS user_posts
ON group_users.id=user_posts.group_user_id
INNER JOIN comments AS comments
ON group_users.id=comments.group_user_id"""

    expected_result1 = """
INNER JOIN user_posts AS user_posts
ON group_users.id=user_posts.group_user_id"""
    self.assertTrue(GroupUser().build_assoc(case1) == expected_result1)
    self.assertTrue(GroupUser().build_assoc(case2) == expected_result2)

  def test_build_sort(self):
    expected_result1 = " ORDER BY id"
    expected_result2 = " ORDER BY id LIMIT 5"
    expected_result3 = " ORDER BY id LIMIT 10 OFFSET 10"
    expected_result4 = " LIMIT 10 OFFSET 10"
    expected_result5 = " OFFSET 10"
    expected_result6 = ""

    self.assertTrue(self.collection.build_sort({"order": "id"}) == expected_result1)
    self.assertTrue(self.collection.build_sort({"order": "id", "limit": 5}) == expected_result2)
    self.assertTrue(self.collection.build_sort({"order": "id", "limit": 10, "offset": 10}) == expected_result3)
    self.assertTrue(self.collection.build_sort({"limit": 10, "offset": 10}) == expected_result4)
    self.assertTrue(self.collection.build_sort({"offset": 10}) == expected_result5)
    self.assertTrue(self.collection.build_sort({}) == expected_result6)
