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

  def get_validations(self):
    return self.__validations

  def add_validations(self, *args, **kwargs):
    if not args:
      raise ValidationError("At least one field is required", "No argument is passed in add_validations function.")
    if not kwargs:
      raise ValidationError("At least one condition is required", "No argument is passed in add_validations function.")
    if "presence" in kwargs:
      if not isinstance(kwargs["presence"], bool):
        raise TypeError("Type mismatch", "Presence takes a boolean")
      for field in args:
        self.__add_validations(field, "presence", kwargs["presence"])

    if "uniqueness" in kwargs:
      if not isinstance(kwargs["uniqueness"], bool):
        raise TypeError("Type mismatch", "Uniqueness takes a boolean")
      for field in args:
        self.__add_validations(field, "uniqueness", kwargs["uniqueness"])

    if "inclusion" in kwargs:
      if not isinstance(kwargs["inclusion"], list):
        raise TypeError("Type mismatch", "Inclusion takes a list")

      for field in args:
        self.__add_validations(field, "inclusion", kwargs["inclusion"])

    if "length" in kwargs:
      if not isinstance(kwargs["length"], dict):
        raise TypeError("Type mismatch", "Length has to be a dict with max and min")

      for field in args:
        self.__add_validations(field, "length", kwargs["length"])
    # if "allow_none" in kwargs:
    #   if not isinstance(kwargs["allow_none"], bool):
    #     raise TypeError("Wrong argument", "Length has to be a dict with max and min")

    #   for field in args:
    #     self.__add_validations(field, "allow_none", kwargs["allow_none"])
    if "range" in kwargs:
      if not isinstance(kwargs["range"], dict):
        raise TypeError("Type mistch", "Range has to be a dict with max and min")

      for field in args:
        self.__add_validations(field, "range", kwargs["range"])

  def __add_validations(self, field, validation, value):
    if field not in self.__validations:
      self.__validations[field] = {}
    self.__validations[field][validation] = value

  def set_validations(self):
    pass

  def presence(self, field, criteria):
    try:
      validation = getattr(self, field)
      if not validation:
        logger.error("Validation Error: {} must be present".format(field))
      return validation
    except AttributeError:
      return False

  def uniqueness(self, field, criteria):
    try:
      query_str = """
        SELECT * FROM {}
        WHERE {} = '{}'
      """.format(
        self.table_name(),
        field,
        getattr(self, field))
    except AttributeError:
      return False
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
    if not isinstance(val, str):
      raise ValidationError("Type mismatch", "Length validation can only apply on strings")

    b1, b2 = True, True
    if "max" in criteria:
      b1 = len(val) <= criteria["max"]
    if "min" in criteria:
      b2 = len(val) >= criteria["min"]

    validation = b1 and b2
    if not validation:
      logger.error("Validation Error: {} must have a length of...")
    return validation

  def range(self, field, criteria):
    val = getattr(self, field)
    if not isinstance(val, int):
      raise ValidationError("Type mismatch", "Range validation can only apply on numbers")

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
