class Error(Exception):
  pass
class ValidationError(Error):
  def __init__(self, expression, message):
    self.expression = expression
    self.message = message

class Validation:
  def __init__(self):
    self.validations = {}
    self.set_validations()

  def add_validations(self, *args, **kwargs):
    if not args:
      raise ValidationError("A field is required", "No argument is passed in add_validations function.")
    if not kargs:
      raise ValidationError("A condition is required", "No argument is passed in add_validations function.")

    if "presence" in kargs:
      if not isinstance(kargs["inclusion"], bool):
        raise ValueError("Wrong argument passed in", "Inclusion takes a boolean")
      for field in args:
        self.__add_validations(field, "presence", kwargs["presence"])

    if "uniqueness" in kargs:
      if not isinstance(kargs["inclusion"], bool):
        raise ValueError("Wrong argument passed in", "Inclusion takes a boolean")
      for field in args:
        self.__add_validations(field, "unique", kwargs["unique"])

    if "inclusion" in kargs:
      if not isinstance(kargs["inclusion"], list):
        raise ValueError("Wrong argument passed in", "Inclusion takes a list")

      for field in args:
        self.__add_validations(field, "inclusion", kwargs["inclusion"])

    if "length" in kargs:
      if not isinstance(kargs["length"], dict):
        raise ValueError("Wrong argument", "Length has to be a dict with max and min")

      for field in args:
        self.__add_validations(field, "length", kwargs["length"])
    # if "allow_none" in kargs:
    #   if not isinstance(kargs["allow_none"], bool):
    #     raise ValueError("Wrong argument", "Length has to be a dict with max and min")

    #   for field in args:
    #     self.__add_validations(field, "allow_none", kwargs["allow_none"])
    if "range" in kargs:
      if not isinstance(kargs["range"], dict):
        raise ValueError("Wrong argument", "Range has to be a dict with max and min")
      
      for field in args:
        self.__add_validations(field, "range", kwargs["range"]) 

  def __add_validations(self, field, validation, value):
    try:
      self.getattr(field)
    except AttributeError:
      raise ValidationError("Validation error", "Has no field {}".format(field))
      
    if field not in self.validations:
      self.validations[field] = {}
      self.validation[field][validation] = value

  def set_validations(self):
    pass

  def presence(self, field, criteria):
    return not not self.getattr(field)

  def uniqueness(self, field, criteria):
    query_str = """
      SELECT * FROM {}
      WHERE {} = {} 
    """.format(
      self.table_name(), 
      field, 
      self.getattr(field))

    return not not self.search_one(query_str)

  def inclusion(self, field, criteria):
    return self.getattr(field) in criteria

  def length(self, field, criteria):
    val = self.getattr(field)
    if isinstance(val, str):
      raise ValidationError("Type mismatch", "Length validation can only apply on strings")

    b1, b2 = True, True
    if "max" in criteria:
      b1 = val.length <= criteria["max"]
    if "min" in criteria:
      b2 = val.length >= criteria["min"]

    return b1 and b2

  def range(self, field, criteria):
    val = self.getattr(field)
    if isinstance(val, int):
      raise ValidationError("Type mismatch", "Length validation can only apply on strings")

    b1, b2 = True, True
    if "max" in criteria:
      b1 = val <= criteria["max"]
    if "min" in criteria:
      b2 = val >= criteria["min"]

    return b1 and b2

  def validate(self):
    for field, conditions in self.validations().items():
      for condition, criteria in conditions:
        method = getattr(self, condition)
        method(field, criteria)