class Error(Exception):
  pass

class ValidationError(Error):
  def __init__(self, expression, message):
    self.expression = expression
    self.message = message

class Validation(object):
  _instance = None
  _initiated = 0
  _validations = {}

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(Validation, cls).__new__(cls, *args, **kwargs)

    return cls._instance

  def __init__(self):
    self.__class__._initiated += 1

  @classmethod
  def get_validations(self, callee_class):
    if callee_class in Validation._validations:
      return Validation._validations[callee_class]

    return {}

  def add_validations(self, callee_class, *args, **kwargs):
    if self.__class__._initiated > 1:
      return

    if not args:
      raise ValidationError("At least one field is required", "No argument is passed in add_validations function.")
    if not kwargs:
      raise ValidationError("At least one condition is required", "No argument is passed in add_validations function.")

    validations = [
      { "validation": "presence", "type": bool, "error": "Presence requires a boolean" },
      { "validation": "uniqueness", "type": bool, "error": "Uniqueness requires a boolean" },
      { "validation": "inclusion", "type": list, "error": "Inclusion requires a list" },
      { "validation": "length", "type": dict, "error": "Length has to be a dict with max and/or min" },
      { "validation": "range", "type": dict, "error": "Length has to be a dict with max and/or min" },
    ]
    for validation in validations:
      validation_type = validation["validation"]

      if validation_type in kwargs:
        if not isinstance(kwargs[validation_type], validation["type"]):
          raise TypeError("Type mismatch", validation["error"])
        for field in args:
          self.__add_validations(callee_class, field, validation_type, kwargs[validation_type])

  def __add_validations(self, callee_class, field, validation, value):
    if callee_class not in Validation._validations:
      Validation._validations[callee_class] = {}

    if field not in Validation._validations[callee_class]:
      Validation._validations[callee_class][field] = {}
    Validation._validations[callee_class][field][validation] = value
