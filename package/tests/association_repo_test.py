import unittest
from . import AssociationRepo as Association

class TestAssociationRepoMethods(unittest.TestCase):
  def test_adding_default_has_many_association(self):
    associations = Association()
    associations.has_many("GroupUser", "UserPosts")

    added_associations = associations.get_associations("GroupUser")
    self.assertFalse(added_associations == {})
    self.assertTrue("user_posts" in added_associations)

    user_posts_association = added_associations["user_posts"]
    self.assertTrue(user_posts_association["type"] == "has_many")
    self.assertTrue(user_posts_association["foreign_key"] == "group_user_id")
    self.assertTrue(user_posts_association["primary_key"] == "id")
    self.assertTrue(user_posts_association["foreign_class"] == "UserPost")
    self.assertTrue(user_posts_association["primary_class"] == "GroupUser")

  def test_adding_default_belongs_to(self):
    associations = Association()
    associations.belongs_to("UserPost", "GroupUser")

    added_associations = associations.get_associations("UserPost")
    self.assertFalse(added_associations == {})
    self.assertTrue("group_users" in added_associations)

    group_user_association = added_associations["group_users"]
    self.assertTrue(group_user_association["type"] == "belongs_to")
    self.assertTrue(group_user_association["foreign_key"] == "group_user_id")
    self.assertTrue(group_user_association["primary_key"] == "id")
    self.assertTrue(group_user_association["primary_class"] == "GroupUser")
    self.assertTrue(group_user_association["foreign_class"] == "UserPost")

if __name__ == "__main__":
  unittest.main()
