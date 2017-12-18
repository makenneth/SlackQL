CONSTRAINTS = {
  "check": lambda exp: "CHECK ({})".format(exp),
  "primary_key": lambda tup: "PRIMARY KEY ({})".format(", ".join(tup)),
  "foreign_key": lambda tup: "FOREIGN KEY ({})".format(", ".join(tup)),
  "unique": lambda tup: "UNIQUE ({})".format(", ".join(tup)),
  "exclude": lambda tup: "{}".format(", ".join(tup))
}

ADDITIONAL = {
  "deferrable": {
    "convert": lambda bool: "DEFERRABLE" if bool else "NOT DEFERRABLE",
    "values": [True, False]
  },
  "initially": {
    "convert": lambda value: "INITIALLY {}".format(value.upper()),
    "values": ["deferred", "immediate"]
  },
  "on_delete": {
    "convert": lambda value: "ON DELETE {}".format(value.upper()),
    "values": ["cascade", "restrict"]
  }
}

class Table:
  def __init__(self, name, **kwargs):
    fields, indices = self.parse_datatypes(name, kwargs)
    self.name = name
    self.fields = fields
    self.constraints = []
    self.indices = indices

  def parse_datatypes(self, name, options):
    indices, fields = [], []
    for field, datatype in options.items():
      field_clause, index_clause = datatype(name, field)
      fields.append(field_clause)
      if index_clause:
        indices.append(index_clause)

    return fields, indices

  def generate_command(self):
    lines = ",\n    ".join(self.fields + self.constraints)

    return """CREATE TABLE {} (
    {}
);""".format(self.name, lines)

  def add_foreign_constraint(self, value, options):
    constraint = CONSTRAINTS["foreign_key"](value)
    if "on_delete" in options:
      on_delete_dict = ADDITIONAL["on_delete"]
      on_delete_val = options["on_delete"]
      if on_delete_val not in on_delete_dict["values"]:
        raise ValueError("Valid arguments for on_delete are".format(" ".join(on_delete_dict["values"])))
      return constraint + " " + on_delete_dict["convert"](options["on_delete"])

    return constraint

  def add_constraint(self, **kwargs):
    constraint_strs = []
    for constraint, value in kwargs.items():
      if constraint == "name":
        constraint_strs.insert(0, "CONSTRAINT {}".format(value))
      elif constraint in CONSTRAINTS:
        if constraint == "foreign_key" :
          constraint_strs.append(self.add_foreign_constraint(value, kwargs))
        else:
          constraint_strs.append(CONSTRAINTS[constraint](value))

      elif constraint in ADDITIONAL:
        valid_options = ADDITIONAL[constraint]["values"]
        if value in valid_options:
          if constraint != "on_delete":
            constraint_strs.append(ADDITIONAL[constraint]["convert"](value))
        else:
          raise ValueError("Valid arguments for {} are".format(constraint, " ".join(valid_options)))
      else:
        raise ValueError("Constraint {}: not valid".format(constraint))
    self.constraints.append((" ").join(constraint_strs))

    return self

  def add_index(self, **kwargs):
    return self
