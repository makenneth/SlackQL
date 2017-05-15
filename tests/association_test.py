import os, sys, unittest
sys.path.append(os.path.abspath(".."))
import SlackQL

class TestAssociationMethods(unittest.TestCase):
  def test_adding_default_has_many_association(self):
    class GroupUser(SlackQL.Association): pass
    associations = GroupUser()
    associations.has_many("UserPosts")

    self.assertTrue("user_posts" in associations._associations)
    added_associations = associations._associations["user_posts"]

    self.assertTrue(added_associations["foreign_key"] == "group_user_id")
    self.assertTrue(added_associations["primary_key"] == "id")
    self.assertTrue(added_associations["assoc_class"] == "UserPost")

  def test_adding_default_belongs_to(self):
    class UserPost(SlackQL.Association): pass
    associations = UserPost()
    associations.belongs_to("GroupUser")

    self.assertTrue("group_users" in associations._associations)
    added_associations = associations._associations["group_users"]

    self.assertTrue(added_associations["foreign_key"] == "group_user_id")
    self.assertTrue(added_associations["primary_key"] == "id")
    self.assertTrue(added_associations["assoc_class"] == "GroupUser")

if __name__ == "__main__":
  unittest.main()
