from .table import Table
from .column import Column

# should update schema every time database is change
# maintain a database and create migrations with name of dates? or some sort of serial
class Migration:
  def __init__(self):
    self.migrations = []

  def create_table(self, name, **kwargs):
    new_migration = Table(name, **kwargs)
    self.migrations.append(new_migration)
    return new_migration

  def add_column(self, name, **kwargs):
    new_migration = Column(name, "add", **kwargs)
    self.migrations.append(new_migration)
    return new_migration

  def remove_column(self, name, **kwargs):
    new_migration = Column(name, "remove", **kwargs)
    self.migrations.append(new_migration)
    return new_migration

  def change_column(self, name, **kwargs):
    new_migration = Column(name, "alter", **kwargs)
    self.migrations.append(new_migration)
    return new_migration

    #

