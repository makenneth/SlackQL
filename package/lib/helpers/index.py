import inflection

def format_clause_value(val):
  return str(val) if type(val) != str else "'{}'".format(val)

def class_to_table(class_name):
  return inflection.pluralize(inflection.underscore(class_name))

def relation_to_class(relation):
  return inflection.singularize(inflection.camelize(relation))
