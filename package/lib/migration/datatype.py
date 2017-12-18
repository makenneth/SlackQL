VALID_TYPES = {
  "int": True,
  "date": True,
  "text": True,
  "varchar": True,
  "char": True,
  "timestamp": True,
  "bool": True,
  "serial": True
}

class Datatype(object):
  def __init__(self, datatype, **kwargs):
    self.verify_type(datatype)
    self.datatype = datatype
    self.length = kwargs.get("length", None)

  def verify_type(self, datatype):
    if datatype not in VALID_TYPES:
      raise AttributeError("Datatype {} is not valid or currently not supported".format(datatype))

  def to_str(self):
    return self.datatype.upper() + ("({})".format(self.length) if self.length else "")
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

