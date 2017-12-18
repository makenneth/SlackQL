from .constraint import Constraint

class TableMetaClass(type):
  def __getattr__(self, key):
    if key in ["alter", "drop", "create"]:
      def wrapper(*args, **kwargs):
        return Table(*args, **kwargs)
      return wrapper
    raise AttributeError(key)

class Table(metaclass=TableMetaClass):
  def __init__(self, method, name, **kwargs):
    self.name = name
    self.options = kwargs
    self.method = method
    self.constraints = []

  def parse_datatypes(self):
    indices, fields = [], []
    for field, column in self.options.items():
      field_clause, index_clause = column.generate_command(self.name, field)
      fields.append(field_clause)
      if index_clause:
        indices.append(index_clause)

    return fields, indices

  def generate_command(self):
    if self.method == "create":
      fields, indices = self.parse_datatypes()
      lines = ",\n    ".join(fields + self.constraints)

      return """CREATE TABLE {} (
      {}
  );""".format(self.name, lines)

    elif self.method == "drop":
      return """DROP TABLE {}{}""".format(
        self.name,
        " CASCADE" if self.options.get("cascade", False) else ""
      )
    elif self.method == "alter":
      fields = [column.generate_command(self.name, field) for field, column in self.options.items()]

      return """ALTER TABLE {}{}""".format(
        ",\n\t".join(fields),
        self.name
      )

  def add_index(self, **kwargs):
    return self

  def add_constraint(self, **kwargs):
    self.constraints.append(Constraint.table(kwargs))

    return self
