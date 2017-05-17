class Validation:
  _instance = None
  _initiated = 0

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(Validation, cls).__new__(cls, *args, **kwargs)

    return cls._instance

  def __init__(self):
    self.__class__._initiated += 1
    self.__validations = {}

  def get_validations(self):
    return self.__validations

  def add_validations(self, *args, **kwargs):
    if self.__class__._initiated > 1:
      return

    print("adding validations")
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
