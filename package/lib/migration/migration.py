from .table import Table

class Migration:
  _migrations = []
  def __new__(cls, *args, **kwargs):
    return cls

  @classmethod
  def create_table(self, name, **kwargs):
    # maybe a table class? or simply a migration action class
    # then add to _migrations
    new_migration = Table(name, kwargs)
    _migrations.append(new_migration)
    return new_migration


  @classmethod
  def add_column(self, name, **kwargs):
    pass

  @classmethod
  def remove_column(self, name, **kwargs):
    pass

  @classmethod
  def change_column(self, name, **kwargs):
    pass


