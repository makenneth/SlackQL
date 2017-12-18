from .table import Table
from .column import Column

class Migration:
  def __init__(self):
    self.migrations = []

  def create_table(self, name, **kwargs):
    new_migration = Table.create(name, **kwargs)
    self.migrations.append(new_migration)
    return new_migration

  def drop_table(self, *args, **kwargs):
    self.migrations.append("DROP TABLE {}{}".format(
      ", ".join(args),
      " CASCADE" if kwargs.get("cascade", False) else "")
    )

  def add_column(self, name, **kwargs):
    columns = {}
    for name, column in kwargs.items():
      columns["name"] = column.set_method("add")
    new_migration = Table.alter(name, **column)
    self.migrations.append(new_migration)
    return new_migration

  def drop_column(self, name, **kwargs):
    columns = {}
    for name, column in kwargs.items():
      columns["name"] = column.set_method("drop")
    new_migration = Table.drop(name, **columns)
    self.migrations.append(new_migration)
    return new_migration

  def change_column(self, name, **kwargs):
    columns = {}
    for name, column in kwargs.items():
      if not column.method:
        columns["name"] = column.set_method("alter")
    new_migration = Table.alter(name, **columns)
    self.migrations.append(new_migration)
    return new_migration

  def rename_column(self, column, new_name):
    columns = {column: Column({"new_name": new_name}, None, "rename")}
    new_migration = Table.alter(name, **columns)
    self.migrations.append(command)
    return new_migration

  def set_schema(self, schema_name):
    pass

  def migrate(self):
    pass
    # Execute all the migrations
    # Create entry in db

    # slackql --migrate
    # will first fetch the entries of migrations
    # then check the list of files, find the last migrated files
    # migrate -> set them to true if success

    # table
    # id | datetime | success |
    # query ("SELECT * FROM

