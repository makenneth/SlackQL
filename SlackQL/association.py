import inflection

class Association:
  def __init__(self):
    self._associations = {}

  def __getattr__(self, name):
    return "Unrecognized association: {}".format(name)

  def has_many(self, assoc_table, **kwargs):
    # By user table
    # assoc_table  "UserPosts"
    # class_name "UserPost"
    # table_name user_posts
    # f_k inflection.underscore(self.__class__.__name__)  + "_id"
    # f_k user_id
    # p_k id (for user table)
    class_name = inflection.singularize(assoc_table)
    table_name = inflection.underscore(assoc_table)
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = inflection.underscore(self.__class__.__name__) + "_id" if "foreign_key" not in kwargs else kwargs["foreign_key"]

    self._associations[table_name] = {
      "type": "has_many",
      "assoc_class": inflection.singularize(assoc_table),
      "primary_key": p_key,
      "foreign_key": f_key
    }

  def belongs_to(self, assoc_table, **kwargs):
    # By user_posts table
    # assoc_table "GroupUser"
    # class_name "GroupUser"
    # table_name "group_users"
    # f_k group_user_id
    # p_k id
    table_name = inflection.underscore(inflection.pluralize(assoc_table))
    p_key = "id" if "primary_key" not in kwargs else kwargs["primary_key"]
    f_key = "{}_id".format(inflection.underscore(assoc_table)) if "foreign_key" not in kwargs else kwargs["foreign_key"]

    self._associations[table_name] = {
      "type": "belongs_to",
      "assoc_class": assoc_table,
      "primary_key": p_key,
      "foreign_key": f_key
    }

  def has_many_through(self, assoc_table, **kwargs):
    pass

