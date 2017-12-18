from .table import Table
from .column import Column

# should update schema every time database is change
# maintain a database and create migrations with name of dates? or some sort of serial
class Migration:
  def __init__(self):
    _migrations = []

  @classmethod
  def create_table(self, name, **kwargs):
    new_migration = Table(name, kwargs)
    self._migrations.append(new_migration)
    return new_migration

  @classmethod
  def add_column(self, name, **kwargs):
    new_migration = Column(name, "add", **kwargs)
    self._migrations.append(new_migration)
    return new_migration

  @classmethod
  def remove_column(self, name, **kwargs):
    new_migration = Column(name, "remove", **kwargs)
    self._migrations.append(new_migration)
    return new_migration

  @classmethod
  def change_column(self, name, **kwargs):
    new_migration = Column(name, "alter", **kwargs)
    self._migrations.append(new_migration)
    return new_migration

    #

