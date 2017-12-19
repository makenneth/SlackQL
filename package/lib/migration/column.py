from .constraint import Constraint
from .datatype import Datatype
import json

class ColumnMetaClass(type):
  def __getattr__(self, key):
    if key in ["set"]:
      def wrapper(*args, **kwargs):
        return Column(kwargs, None, "set")
      return wrapper
    elif key in ["varchar", "char"]:
      # currying the length since it requires length for varchar and char
      def variable_length_wrapper(*args1):
        def wrapper(*args, **kwargs):
          return Column(kwargs, Datatype(key, length=args1[0]))

        if len(args1) == 0:
          raise TypeError("{}() missing 1 required positional argument: 'length'".format(key))

        return wrapper
      return variable_length_wrapper
    else:
      def wrapper(*args, **kwargs):
        return Column(kwargs, Datatype(key))
      return wrapper

class Column(metaclass=ColumnMetaClass):
  def __init__(self, options, datatype = None, method = None):
    self.datatype = datatype
    self.options = options
    self.method = method

  def set_method(self, method):
    self.method = method
    return self

  def generate_command(self, table, column):
    if self.method == None or self.method == "add" or self.method == "alter":
      index_clause = None

      if "index" in self.options:
        index_clause = self.get_index(table, column, self.options["index"])

      return (self.get_column_clause(column, self.method), index_clause)
    elif self.method == "drop":
      words = ["DROP COLUMN"]
      if self.options.get("if_exists", False):
        words.append("IF EXISTS")
      words.append(column)
      if "on_delete" in self.options:
        on_delete = self.options["on_delete"]
        words.append("ON DELETE")
        if on_delete in ["restrict", "cascade"]:
          words.append(on_delete.upper())
        else:
          raise ValueError("on_delete has to be one of 'restrict' and 'cascade'")
      return (" ".join(words),)
    elif self.method == "rename":
      return ("RENAME COLUMN {} TO {}".format(column, self.options["new_name"]),)

    elif self.method == "set":
      constraint, value = list(self.options.items())[0]
      if constraint not in ["null", "default"]:
        raise ValueError("""
        {} is not something you can set (yet). Valid options are ["null", "default"].
        """.format(constraint))
      change = ""
      if constraint == "default":
        change = "{} DEFAULT{}".format(
          "SET" if value else "DROP",
          " {}".format(json.dumps(value)) if value else ""
        )
      elif constraint == "null":
        change = "{} NOT NULL".format("DROP" if value else "SET")

      return ("ALTER COLUMN {} {}".format(column, change),)

  def verify_options(self, options):
    if "using_method" in options:
      if options["using_method"] not in ["btree", "hash", "gist", "spgist", "gin", "brin"]:
        raise ValueError("""
        {} not a valid value for 'using_method'. Valid options are: 'btree', 'hash', 'gist', 'spgist', 'gin', and 'brin'
        """.format(options["using_method"]))

  def get_index(self, table, column, options):
    if type(options) is bool:
      return "CREATE INDEX ON {table_name} ({column_name});".format(
        table_name=table, column_name=column
      )
    else:
      self.verify_options(options)
      return """
      CREATE{unique} INDEX{concurrently}{if_not_exists}{name} ON {table_name}{using_method} ({column_name});
      """.format(
        name=" {}".format(options["name"]) if "name" in options else "",
        table_name=table,
        column_name=column,
        using_method=" USING {}".format(options["using_method"]) if "using_method" in options else "",
        unique=" UNIQUE" if "unique" in options else "",
        concurrently=" CONCURRENTLY" if options.get("concurrently", False) else "",
        if_not_exists=" IF NOT EXISTS" if options.get("if_not_exists", False) else ""
      )

  def get_column_clause(self, column, method = None):
    constraint_clause = Constraint.column(self.options)
    prefix = ""
    if method:
      prefix = "{} COLUMN ".format(method.upper())
    return "{}{} {}{}{}".format(
      prefix,
      column,
      self.datatype.to_str(),
      " " if len(constraint_clause) else "",
      constraint_clause
    )

