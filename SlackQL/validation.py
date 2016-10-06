from . import logger

class Error(Exception):
  pass
class ValidationError(Error):
  def __init__(self, expression, message):
    self.expression = expression
    self.message = message

class Validation:
  def __init__(self):
    self.__validations = {}

  def add_validations(self, *args, **kwargs):
    if not args:
      raise ValidationError("A field is required", "No argument is passed in add_validations function.")
    if not kwargs:
      raise ValidationError("A condition is required", "No argument is passed in add_validations function.")
    if "presence" in kwargs:
      if not isinstance(kwargs["presence"], bool):
        raise ValueError("Wrong argument passed in", "Inclusion takes a boolean")
      for field in args:
        self.__add_validations(field, "presence", kwargs["presence"])

    if "uniqueness" in kwargs:
      if not isinstance(kwargs["uniqueness"], bool):
        raise ValueError("Wrong argument passed in", "Inclusion takes a boolean")
      for field in args:
        self.__add_validations(field, "uniqueness", kwargs["uniqueness"])

    if "inclusion" in kwargs:
      if not isinstance(kwargs["inclusion"], list):
        raise ValueError("Wrong argument passed in", "Inclusion takes a list")

      for field in args:
        self.__add_validations(field, "inclusion", kwargs["inclusion"])

    if "length" in kwargs:
      if not isinstance(kwargs["length"], dict):
        raise ValueError("Wrong argument", "Length has to be a dict with max and min")

      for field in args:
        self.__add_validations(field, "length", kwargs["length"])
    # if "allow_none" in kwargs:
    #   if not isinstance(kwargs["allow_none"], bool):
    #     raise ValueError("Wrong argument", "Length has to be a dict with max and min")

    #   for field in args:
    #     self.__add_validations(field, "allow_none", kwargs["allow_none"])
    if "range" in kwargs:
      if not isinstance(kwargs["range"], dict):
        raise ValueError("Wrong argument", "Range has to be a dict with max and min")
      
      for field in args:
        self.__add_validations(field, "range", kwargs["range"]) 

  def __add_validations(self, field, validation, value):
    try:
      getattr(self, field)
    except AttributeError:
      raise ValidationError("Validation error", "Has no field {}".format(field))
      
    if field not in self.__validations:
      self.__validations[field] = {}
    self.__validations[field][validation] = value

  def set_validations(self):
    pass

  def presence(self, field, criteria):
    validation = getattr(self, field)
    if not validation:
      logger.error("Validation Error: {} must be present".format(field))
    return validation

  def uniqueness(self, field, criteria):
    query_str = """
      SELECT * FROM {}
      WHERE {} = '{}' 
    """.format(
      self.table_name(), 
      field, 
      getattr(self, field))
    validation = not self.search_one(query_str)
    if not validation:
      logger.error("Validation Error: {} must be unique".format(field))
    return validation

  def inclusion(self, field, criteria):
    validation = getattr(self, field) in criteria
    if not validation:
      logger.error("Validation Error: {} must be one of {}".format(field, criteria))
    return validation

  def length(self, field, criteria):
    val = getattr(self, field)
    if isinstance(val, str):
      raise ValidationError("Type mismatch", "Length validation can only apply on strings")

    b1, b2 = True, True
    if "max" in criteria:
      b1 = val.length <= criteria["max"]
    if "min" in criteria:
      b2 = val.length >= criteria["min"]

    validation = b1 and b2
    if not validation:
      logger.error("Validation Error: {} must have a length of...")
    return validation

  def range(self, field, criteria):
    val = getattr(self, field)
    if isinstance(val, int):
      raise ValidationError("Type mismatch", "Length validation can only apply on strings")

    b1, b2 = True, True
    if "max" in criteria:
      b1 = val <= criteria["max"]
    if "min" in criteria:
      b2 = val >= criteria["min"]

    return b1 and b2

  def validate(self):
    if not self.__validations:
      return True

    for field, conditions in self.__validations.items():
      for condition, criteria in conditions.items():
        method = getattr(self, condition)
        if not method(field, criteria):
          return False

    return True
