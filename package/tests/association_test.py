import unittest
from . import Association

class TestAssociationMethods(unittest.TestCase):
  def test_adding_default_has_many_association(self):
    class GroupUser(Association): pass
    associations = GroupUser()
    associations.has_many("UserPosts")

    self.assertTrue("user_posts" in associations._associations)
    added_associations = associations._associations["user_posts"]

    self.assertTrue(added_associations["foreign_key"] == "group_user_id")
    self.assertTrue(added_associations["primary_key"] == "id")
    self.assertTrue(added_associations["foreign_class"] == "UserPost")
    self.assertTrue(added_associations["primary_class"] == "GroupUser")

  def test_adding_default_belongs_to(self):
    class UserPost(Association): pass
    associations = UserPost()
    associations.belongs_to("GroupUser")

    self.assertTrue("group_users" in associations._associations)
    added_associations = associations._associations["group_users"]

    self.assertTrue(added_associations["foreign_key"] == "group_user_id")
    self.assertTrue(added_associations["primary_key"] == "id")
    self.assertTrue(added_associations["primary_class"] == "GroupUser")
    self.assertTrue(added_associations["foreign_class"] == "UserPost")

if __name__ == "__main__":
  unittest.main()
