from . import logger, repository

class Validation:
  def __init__(self):
    self.__validations = repository.Validation()

  def add_validations(self, *args, **kwargs):
    self.__validations.add_validations(self.__class__.__name__, *args, **kwargs)

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
    if not isinstance(val, str) and not isinstance(val, list):
      raise repository.ValidationError("Type mismatch", "Length validation can only apply on strings or lists")

    b1, b2 = True, True
    if "max" in criteria:
      b1 = len(val) <= criteria["max"]
    if "min" in criteria:
      b2 = len(val) >= criteria["min"]

    validation = b1 and b2
    if not validation:
      logger.error("Validation Error: {} must have a length between {} and {}".format(field, criteria["min"], criteria["max"]))
    return validation

  def range(self, field, criteria):
    val = getattr(self, field)
    if not isinstance(val, int):
      raise repository.ValidationError("Type mismatch", "Range validation can only apply on numbers")

    b1, b2 = True, True
    if "max" in criteria:
      b1 = val <= criteria["max"]
    if "min" in criteria:
      b2 = val >= criteria["min"]

    return b1 and b2

  def validate(self):
    validations = repository.Validation.get_validations(self.__class__.__name__)
    if not validations:
      return True

    for field, conditions in validations.items():
      for condition, criteria in conditions.items():
        method = getattr(self, condition)
        if not method(field, criteria):
          return False

    return True
