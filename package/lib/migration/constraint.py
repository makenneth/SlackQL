# to split it between column and table
import json

def references(arg):
  if type(arg) == str:
    return "REFERENCES {}".format(arg)
  elif type(arg) == dict:
    ref_str = ""
    if "table" in arg:
      ref_str += "REFERENCES {}{}".format(arg["table"], "({})".format(arg["key"]) if "key" in arg else "")
    else:
      raise ValueError("Must include table in references dict")

    if "match" in arg:
      if arg["match"] in ["full", "partial", "simple"]:
        ref_str += " MATCH {}".format(arg["match"].upper())
      else:
        raise ValueError("Value with key 'match' must be one of 'full', 'partial', or 'simple'.")

    for constraint in ["on_delete", "on_update"]:
      if constraint in arg:
        if arg[constraint] in ["cascade", "restrict"]:
          ref_str += " ON DELETE {}".format(arg[constraint].upper())
        else:
          raise ValueError("Value with key '{}' has to be either 'cascade' or 'restrict'.".format(constraint))

    return ref_str

TABLE_CONSTRAINTS = {
  "name": lambda name: "CONSTRAINT {}".format(name),
  "check": lambda exp: "CHECK ({})".format(exp),
  "primary_key": lambda tup: "PRIMARY KEY ({})".format(", ".join(tup)),
  "foreign_key": lambda tup: "FOREIGN KEY ({})".format(", ".join(tup)),
  "unique": lambda tup: "UNIQUE ({})".format(", ".join(tup)),
  "exclude": lambda tup: "{}".format(", ".join(tup))
}

TABLE_ADDITIONAL = {
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

COLUMN_CONSTRAINTS = {
  "check": lambda exp: "CHECK ({})".format(exp),
  "primary_key": lambda bool: "PRIMARY KEY" if bool else "",
  "references": references,
  "unique": lambda bool: "UNIQUE" if bool else "",
  "exclude": lambda tup: "{}".format(", ".join(tup)),
  "default": lambda exp: "DEFAULT {}".format(json.dumps(exp)),
  "null": lambda bool: "NOT NULL" if not bool else ""
}

class Constraint:
  @classmethod
  def column(cls, options):
    constraint_clause = []
    for constraint, value in options.items():
      if constraint in COLUMN_CONSTRAINTS:
        constraint_clause.append(COLUMN_CONSTRAINTS[constraint](value))
      elif constraint != "index":
        raise ValueError("Constraint {} not supported".format(constraint))

    return " ".join(constraint_clause)

  @classmethod
  def table(cls, options):
    constraint_strs = []
    for constraint, value in options.items():
      if constraint == "name":
        constraint_strs.insert(0, TABLE_CONSTRAINTS["name"](value))
      elif constraint in TABLE_CONSTRAINTS:
        if constraint == "foreign_key" :
          constraint_strs.append(cls.format_foreign_constraint(value, options))
        else:
          constraint_strs.append(TABLE_CONSTRAINTS[constraint](value))

      elif constraint in TABLE_ADDITIONAL:
        valid_options = TABLE_ADDITIONAL[constraint]["values"]
        if value in valid_options:
          if constraint != "on_delete":
            constraint_strs.append(TABLE_ADDITIONAL[constraint]["convert"](value))
        else:
          raise ValueError("Valid arguments for {} are".format(constraint, " ".join(valid_options)))
      else:
        raise ValueError("Constraint {}: not valid".format(constraint))
    return " ".join(constraint_strs)

  @classmethod
  def format_foreign_constraint(cls, value, options):
    constraint = TABLE_CONSTRAINTS["foreign_key"](value)
    if "on_delete" in options:
      on_delete_dict = TABLE_ADDITIONAL["on_delete"]
      on_delete_val = options["on_delete"]
      if on_delete_val not in on_delete_dict["values"]:
        raise ValueError("Valid arguments for on_delete are".format(" ".join(on_delete_dict["values"])))
      return constraint + " " + on_delete_dict["convert"](options["on_delete"])

    return constraint
