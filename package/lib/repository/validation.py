class Error(Exception):
  pass

class ValidationError(Error):
  def __init__(self, expression, message):
    self.expression = expression
    self.message = message

class Validation(object):
  _instance = None
  _initiated = 0

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(Validation, cls).__new__(cls, *args, **kwargs)

    return cls._instance

  def __init__(self):
    self.__class__._initiated += 1
    self.__validations = {}

  def get_validations(self, callee_class):
    if callee_class in self.__validations:
      return self.__validations[callee_class]

    return {}

  def add_validations(self, callee_class, *args, **kwargs):
    if self.__class__._initiated > 1:
      return

    if not args:
      raise ValidationError("At least one field is required", "No argument is passed in add_validations function.")
    if not kwargs:
      raise ValidationError("At least one condition is required", "No argument is passed in add_validations function.")
    if "presence" in kwargs:
      if not isinstance(kwargs["presence"], bool):
        raise TypeError("Type mismatch", "Presence takes a boolean")
      for field in args:
        self.__add_validations(callee_class, field, "presence", kwargs["presence"])

    if "uniqueness" in kwargs:
      if not isinstance(kwargs["uniqueness"], bool):
        raise TypeError("Type mismatch", "Uniqueness takes a boolean")
      for field in args:
        self.__add_validations(callee_class, field, "uniqueness", kwargs["uniqueness"])

    if "inclusion" in kwargs:
      if not isinstance(kwargs["inclusion"], list):
        raise TypeError("Type mismatch", "Inclusion takes a list")

      for field in args:
        self.__add_validations(callee_class, field, "inclusion", kwargs["inclusion"])

    if "length" in kwargs:
      if not isinstance(kwargs["length"], dict):
        raise TypeError("Type mismatch", "Length has to be a dict with max and min")

      for field in args:
        self.__add_validations(callee_class, field, "length", kwargs["length"])
    # if "allow_none" in kwargs:
    #   if not isinstance(kwargs["allow_none"], bool):
    #     raise TypeError("Wrong argument", "Length has to be a dict with max and min")

    #   for field in args:
    #     self.__add_validations(callee_class, field, "allow_none", kwargs["allow_none"])
    if "range" in kwargs:
      if not isinstance(kwargs["range"], dict):
        raise TypeError("Type mistch", "Range has to be a dict with max and min")

      for field in args:
        self.__add_validations(callee_class, field, "range", kwargs["range"])

  def __add_validations(self, callee_class, field, validation, value):
    if callee_class not in self.__validations:
      self.__validations[callee_class] = {}

    if field not in self.__validations[callee_class]:
      self.__validations[callee_class][field] = {}
    self.__validations[callee_class][field][validation] = value