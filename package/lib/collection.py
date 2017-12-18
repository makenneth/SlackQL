import inflection
import numbers
from .searchable import Searchable
from .validation import Validation
from .association import Association
from . import Logger, db, repository, helpers
from time import time

class Collection(Searchable, Validation, Association):
  def columns(self):
    if not self.__columns:
      self.__columns = repository.Columns.get_columns(self.table_name())
    return self.__columns

  def __init__(self, **kwargs):
    super(Collection, self).__init__()
    if self.set_validations:
      self.set_validations()
    if self.set_associations:
      self.set_associations()
    for column in self.columns():
      setattr(self, column, kwargs[column] if column in kwargs else None)

  def __str__(self):
    instance_data = []
    for col in self.columns():
      attr_val = getattr(self, col)
      instance_data.append("{}={}".format(col, helpers.format_clause_value(attr_val)))

    for key, value in repository.Association.get_associations(self.__class__.__name__).items():
      if hasattr(self, key):
        attr_val = getattr(self, key)
        instance_data.append("{}={}".format(key, helpers.format_clause_value(attr_val)))

    return Logger.representation("<class '{class_name}' {{{info}}}>".format(
      class_name=self.__class__.__name__,
      info=(", ").join(instance_data)
    ))

  def __repr__(self):
    instance_data = []
    for col in self.columns():
      attr_val = getattr(self, col)
      instance_data.append("{}={}".format(col, helpers.format_clause_value(attr_val)))

    # for key, value in repository.Association.get_associations(self.__class__.__name__).items():
    #   if hasattr(self, key):
    #     attr_val = getattr(self, key)
    #     instance_data.append("{}={}".format(key, helpers.format_clause_value(attr_val)))

    return Logger.representation("<class '{class_name}' {{{info}}}>".format(
      class_name=self.__class__.__name__,
      info=(", ").join(instance_data)
    ))

  def table_name(self, *args):
    if not self.__table:
      if args:
        self.__table = args[0]
      else:
        self.__table = inflection.underscore(inflection.pluralize(self.__class__.__name__))
    return self.__table

  def insert(self, **kwargs):
    values, columns = "", ""
    cursor = db.connection.cursor()
    for i, key in enumerate(kwargs):
      if not i == 0:
        columns += ", "
        values += ", "

      columns += key
      if isinstance(kwargs[key], numbers.Number):
        values += str(kwargs[key])
      else:
        values += "'" + kwargs[key] + "'"

    Logger.time("Transaction begin:")
    sql_str = """INSERT INTO {table_name} ({columns})
              VALUES ({values});""".format(
        table_name=self.table_name(),
        columns=columns,
        values=values
        )
    ####  *** what happens if there are errors ***
    start = time()
    Logger.query(sql_str)
    cursor.execute(sql_str)
    db.connection.commit()
    Logger.complete(start, "Committed")
    self.id = cursor.lastrowid
    return True

  def update(self, **kwargs):
    cursor = db.connection.cursor()
    values = ""

    for i, key in enumerate(kwargs):
      if not i == 0:
        values += ", "

      values += "'{column}={value}'".format(column=key, value=kwargs[key])

    sql_str = """UPDATE {table_name}
              SET {queries}""".format(self.table_name(), values)
    start = time()
    Logger.time("Transaction begin:")
    Logger.query(sql_str)
    cursor.execute(sql_str)
    db.connection.commit()
    Logger.complete(start, "Committed")

    return True

  def destroy(self, id):
    pass

  def save(self, **kwargs):
    attrs = {}
    for key, val in kwargs.items():
      if key in self.columns():
        setattr(self, key, val)

    if not self.validate():
      Logger.warning("ROLLBACK Transaction.")
      return self

    for key, val in self:
      if val and key != "_associations":
        attrs[key] = val

    if "id" in attrs:
      return self.update(**attrs)
    else:
      return self.insert(**attrs)

  def apply_query(self, collection, *args):
    if collection == "all":
      return self.search_all(*args)
    else:
      return self.search_one(*args)

  def search_all(self, query, aggregations, associations):
    query = self.__build_query(query, aggregations)
    cursor = db.connection.cursor()
    start = time()
    cursor.execute(query)
    Logger.time("{0} loads - {1:.2f}ms".format(
      self.__class__.__name__,
      (time() - start) * 1000
    ))
    return self.__get_result(cursor, associations)

  def search_one(self, query, aggregations, associations):
    cursor = db.connection.cursor()
    query = """SELECT {select_clause}
            FROM {table_name}{where_clause}
            LIMIT 1;""".format(
      select_clause=self.__build_select(query, associations),
      table_name=self.table_name(),
      where_clause=self.__build_conds(query)
    )
    Logger.query(query)
    start = time()
    cursor.execute(query)

    Logger.time("{0} loads - {1:.2f}ms".format(
      self.__class__.__name__,
      (time() - start) * 1000
    ))
    columns = [tuple[0] for tuple in cursor.description]
    result = cursor.fetchone()
    if not result:
      Logger.warning("No such entry found")
      return None
    else:
      obj = type(self.__class__.__name__, (Collection,), {})()
      for i in range(len(result)):
        setattr(obj, columns[i], result[i])
      return obj

  def __get_all_key_used(self, assoc_tables, associations):
    referenced_keys = {}
    associations = repository.Association.get_associations(self.__class__.__name__)
    for table in assoc_tables:
      assoc_class = helpers.class_to_table(table.__name__ if type(table) is not str else table)
      if assoc_class in associations:
        association = associations[assoc_class]

        if association["type"] == "belongs_to":
          referenced_keys[association["foreign_key"]] = True
        elif association["type"] == "has_many":
          referenced_keys[association["primary_key"]] = True

    return referenced_keys

  def __fetch_main_result(self, cursor, keys_referenced):
    columns = [tuple[0] for tuple in cursor.description]
    main_class = type(self.__class__.__name__, (Collection,), {})
    result, result_key_reference = [], {}
    for item in cursor.fetchall():
      new_entry = main_class()
      for i in range(len(item)):
        setattr(new_entry, columns[i], item[i])

      for key in keys_referenced:
        if not key in result_key_reference:
          result_key_reference[key] = {}

        result_key_reference[key][getattr(new_entry, key)] = new_entry

      result.append(new_entry)

    return result, result_key_reference

  def __fetch_associations(self, assoc_tables, associations, result, result_reference):
    other_associations = {}
    for table in assoc_tables:
      assoc_class = helpers.class_to_table(table.__name__ if not type(table) == str else table)
      if assoc_class in associations:
        association = associations[assoc_class]

        if association["type"] == "has_many_through":
          source = association["source"]
          if source not in other_associations:
            other_associations[source] = []

          other_associations[source].append(association["relation_names"])

    for table in assoc_tables:
      reference_key, reference_keys = None, []
      other_key, reference_class_name = None, None

      assoc_class = helpers.class_to_table(table.__name__ if not type(table) == str else table)
      if assoc_class not in associations:
        continue
      association = associations[assoc_class]

      if association["type"] == "has_many_through":
        continue
      elif association["type"] == "has_many":
        reference_class_name = association["foreign_class"]
        reference_key = association["primary_key"]
        other_key = association["foreign_key"]
      elif association["type"] == "belongs_to":
        reference_class_name = association["primary_class"]
        reference_key = association["foreign_key"]
        other_key = association["foreign_key"]

      reference_keys = [getattr(r, reference_key) for r in result]
      reference_class = type(reference_class_name, (Collection,), {})
      reference_results = reference_class().within(other_key, reference_keys)

      if table in other_associations:
        reference_results = reference_results.includes(*other_associations[table])
      associated_result_dict = {}

      for item in reference_results:
        key = getattr(item, other_key)
        if not key in associated_result_dict:
          associated_result_dict[key] = []
        associated_result_dict[key].append(item)

      attr_name = inflection.pluralize(inflection.underscore(reference_class_name))
      for key, item in associated_result_dict.items():
        referenced_object = result_reference[reference_key][key]
        setattr(referenced_object, attr_name, item)

  def __get_result(self, cursor, assoc_tables):
    associations = repository.Association.get_associations(self.__class__.__name__)
    keys_referenced = self.__get_all_key_used(assoc_tables, associations)
    result, result_key_reference = self.__fetch_main_result(cursor, keys_referenced)
    if len(assoc_tables) > 0:
      self.__fetch_associations(assoc_tables, associations, result, result_key_reference)

    return result

  def __build_conds(self, query):
    query_str = ""
    if "where" in query:
      query_str += " WHERE {}".format(query["where"])
    if "within" in query:
      query_str += " WHERE " + query["within"] if query_str == "" else " AND " + query["within"]
    if "between" in query:
      query_str += " WHERE {}".format(query["between"]) if query_str == "" else " AND " + query["between"]
    return query_str

  def __build_sort(self, query):
    query_str = ""
    if "order" in query:
      query_str += " ORDER BY {}".format(query["order"])
    if "limit" in query:
      query_str += " LIMIT {}".format(query["limit"])
    if "offset" in query:
      query_str += " OFFSET {}".format(query["offset"])

    return query_str

  def __build_select(self, query, aggregation):
    select_clause = ""
    if "count" in aggregation:
      if aggregation["count"] == "all":
        select_clause += "COUNT(*)"
      else:
        select_clause += (", ").join(["COUNT({})".format(agg) for agg in aggregation["count"]])

    if "select" in query:
      select_clause = query["select"] + " " + select_clause
    elif select_clause == "":
      select_clause = "*"

    return select_clause

  def __build_aggregations(self, aggregations):
    aggregate_str = ""

    if "group" in aggregations:
      aggregate_str += aggregation["group"]

    if "having" in aggregations:
      aggregate_str += aggregation["having"]

    return aggregate_str
  # def build_assoc(self, associations):
  #   assocs = ""

  #   added_associations = repository.Association.get_associations(self.__class__.__name__)
  #   if not added_associations:
  #     return assocs

  #   for join_type, tables in associations.items():
  #     # have to get associations here.. so the key for
  #     # the association repo should be different
  #     # should use something like table_name
  #     # so it can be quickly referenced

  #     for table_name in tables:
  #       if not table_name in added_associations:
  #         Logger.error("Relationship {} not defined".format(table_name))
  #         continue
  #       rel = added_associations[table_name]
  #       assocs += """
  #   {join_type} {join_table_name} AS {join_table_name}
  #   ON {p_c}.{p_k}={f_c}.{f_k}""".format(
  #         join_type=join_type,
  #         join_table_name=table_name,
  #         p_c=self.class_to_table(rel["primary_class"]),
  #         f_c=self.class_to_table(rel["foreign_class"]),
  #         p_k=rel["primary_key"],
  #         f_k=rel["foreign_key"]
  #       )

  #   return assocs

  def __query_assoc(self, relation_name):
    # does relation exists in associations
    associations = repository.Association.get_associations(self.__class__.__name__)
    association = associations[relation_name]
    # is it an indirect relationship?
    if "relation" in association:

      # does the source relation exist?
      if not association["source"] in associations:
        Logger.error("Source relation {} is not defined in {}.".format(association["source"], self.__class__.__name__))
        return None

      source_class_name = helpers.relation_to_class(association["source"])

      # indirect relationship could be through has_many or has_one
      possible_through_relations = [inflection.pluralize(relation_name), inflection.singularize(relation_name)]
      source_associations = repository.Association.get_associations(source_class_name)

      # is the through relation defined in source?
      if not source_associations:
        Logger.error("Relations are not defined in {}.".format(source_class_name))
        return None

      # find the acutal name of the association in source class
      relation_name_in_source = next((rel for rel in possible_through_relations if rel in source_associations), None)
      if not relation_name_in_source:
        Logger.error("Relation {} does not exist in {}.".format(relation_name, source_class_name))
        return None

      source_class = type(source_class_name, (Collection,), {})

      main_source_relation = associations[association["source"]]
      self_ref_key, other_ref_key = None, None

      if main_source_relation["type"] == "has_many":
        self_ref_key = main_source_relation["primary_key"]
        other_ref_key = main_source_relation["foreign_key"]
      else:
        self_ref_key = main_source_relation["foreign_key"]
        other_ref_key = main_source_relation["primary_key"]

      return source_class().includes(relation_name_in_source).where(**{other_ref_key: getattr(self, self_ref_key)}).find_all()
    else:
      class_name = helpers.relation_to_class(relation_name)

      related_class = type(class_name, (Collection,), {})
      self_ref_key, other_ref_key = None, None

      if association["type"] == "has_many":
        self_ref_key = association["primary_key"]
        other_ref_key = association["foreign_key"]
      else:
        self_ref_key = association["foreign_key"]
        other_ref_key = association["primary_key"]

      return related_class().where(**{other_ref_key: getattr(self, self_ref_key)}).find_all()

  def __build_query(self, query, aggregations):
    # assocs = self.build_assoc(associations)
    # alias = self.table_name() if len(associations) > 0 else ""
    # alias_clause = " AS {}".format(self.table_name()) if alias != "" else ""
    # need to account for foreign table
    query_str = """SELECT {} FROM {}{}{}{};""".format(
      self.__build_select(query, aggregations),
      self.table_name(),
      self.__build_conds(query),
      self.__build_sort(query),
      self.__build_aggregations(aggregations)
    )
    Logger.query(query_str)
    return query_str

  def __iter__(self):
    for key, val in self.__dict__.items():
      if "__" not in key:
       yield key, val

  def __getattr__(self, val, *args, **kwargs):
    if val == "belongs_to" or val == "has_many":
      def wrapper(*args, **kwargs):
        getattr(repository.Association, val)(self.__class__.__name__, *args, **kwargs)
      return wrapper

    assoc = repository.Association.get_associations(self.__class__.__name__)
    if assoc and val in assoc:
      return self.__query_assoc(val)
    elif callable(val):
      Logger.error("Invalid method {}".format(val.__name__))
    else:
      return None
