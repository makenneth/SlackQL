# also should have a schema file
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


CONSTRAINTS = {
  "check": lambda exp: "CHECK ({})".format(exp),
  "primary_key": lambda bool: "PRIMARY KEY" if bool else "",
  "references": references,
  "unique": lambda bool: "UNIQUE" if bool else "",
  "exclude": lambda tup: "{}".format(", ".join(tup)),
  "default": lambda exp: "DEFAULT {}".format(json.dumps(exp)),
  "null": lambda bool: "NOT NULL" if not bool else ""
}

ADDITIONAL = {
  "deferrable": {
    "convert": lambda bool: "DEFERRABLE" if bool else "NOT DEFERRABLE",
    "values": [True, False]
  },
  "initially": {
    "convert": lambda value: "INITIALLY {}".format(value.upper()),
    "values": ["deferred", "immediate"]
  }
}

VALID_TYPES = {
  "int": True,
  "date": True,
  "text": True,
  "varchar": True,
  "char": True,
  "timestamp": True,
  "bool": True
}

class DataTypesMetaclass(type):
  def __getattr__(self, key):
    if key in VALID_TYPES:
      def wrapper(*args, **kwargs):
        return self.parse_datatype_options(key, **kwargs)
      return wrapper
    elif key in ["get_index", "get_column_clause", "parse_datatype_options"]:
      def wrapper(*args, **kwargs):
        return getattr(self, key)(*args, **kwargs)
      return wrapper
    raise AttributeError(key)

  def get_index(self, table, column, options):
    if type(options) is bool:
      return "CREATE INDEX ON {table_name} ({column_name});".format(
          table_name=table, column_name=column
      )
    else:
      # ["btree", "hash", "gist", "spgist", "gin", "brin"]
      return """
      CREATE{unique} INDEX{concurrently}{if_not_exists}{name} ON {table_name}{using_method} ({column_name});
      """.format(
        name=" {}".format(options["name"]) if "name" in options else "",
        table_name=table,
        column_name=column,
        using_method=" USING {}".format(options["using_method"]) if "using_method" in options else "",
        unique=" UNIQUE" if "unique" in options else "",
        concurrently=" CONCURRENTLY" if "concurrently" in options else "",
        if_not_exists=" IF NOT EXISTS" if "if_not_exists" in options else ""
      )

  def get_column_clause(self, column, datatype, options):
    constraint_clause = []
    for constraint, value in options.items():
      if constraint in CONSTRAINTS:
        constraint_clause.append(CONSTRAINTS[constraint](value))
      else:
        raise ValueError("{} not suppored".format(constraint))

    return "{} {}{}{}".format(column, datatype.upper(), " " if len(constraint_clause) else "", " ".join(constraint_clause))


  def parse_datatype_options(self, datatype, **kwargs):
    # big problem. we don't have column name
    # we can return a lambda that takes in table and column
    def closure(table, column):
      index_clause = None

      if "index" in kwargs.items():
        index_clause = self.get_index(table, column, kwargs.items()["index"])

      return [self.get_column_clause(column, datatype, kwargs), index_clause]
    return closure

class DBDatatypes(metaclass=DataTypesMetaclass):
  pass

    # ["int", "smallint", "float", "date", "time", "timestamp", "interval", "jsonb", "char(40)"]
    # ##char(n)
##varchar(n)
##text(n)
# int - smallint, int, serial
# float, float, real/float8, numeric, numeric(p, s)
# date
# time
# timestamp
# interval
# timestampz
# box
# line
# point
# lseg
# polygon
# inet
# macaddr

