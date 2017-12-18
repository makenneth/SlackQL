CONSTRAINTS = {
  "check": lambda exp: "CHECK ({})".format(exp),
  "primary_key": lambda tup: "PRIMARY KEY ({})".format(", ".join(x)),
  "foreign_key": lambda tup: "FOREIGN KEY ({})".format(", ".join(x)),
  "unique": lambda tup: "UNIQUE ({})".format(", ".join(x)),
  "exclude": lambda tup: "{}".format(", ".join(tup))
}

ADDITIONAL = {
  "deferrable": {
    "convert": lambda bool: "DEFERRABLE" if bool else "NOT DEFERRABLE",
    "values": [True, False]
  },
  "initially": {
    "convert": lambda value: "INITIALLY {}".format(value),
    "values": ["deferred", "immediate"]
  },
  "on_delete": {
    "convert": lambda value: "ON DELETE {}".format(value),
    "values": ["cascade", "restrict"]
  }
}
class Table:
  def __init__(self, name, **kwargs):
    fields = []
    constraints = []
    self.name = name
    self.fields = fields
    self.constraints = constraints

  def generate_command(self):
    fields = ",\n".join(self.fields)
    constraints = ",\n".join(self.constraints)

    return """CREATE TABLE {} (
      {}{}
      {}
    );""".format(self.name, fields, "," if len(constraints) > 0 else "", constraints)

  def add_constraint(self, **kwargs):
    constraint_strs = []
    for constraint, value in kwargs.items():
      if constraint == "name":
        constraint_strs.insert(0, "CONSTRAINTS {}".format(value))
      elif constraint in CONSTRAINTS:
        str = ""
        if constraint == "foreign_key" and "on_delete" in kwargs:
          str += ADDITIONAL[constraint].convert(value)
        constraint_strs.append(str + CONSTRAINTS[constraint](value))
      elif constraint in ADDITIONAL:
        if value in ADDITIONAL[constraint].values:
          if constraint != "on_delete":
            constraint_strs.append(ADDITIONAL[constraint].convert(value))
        else:
          print("Value {}: not recognized".format(value))
      else:
        print("Constraint {}: not supported".format(constraint))

    self.constraints.append((" ").join(constraint_strs))
