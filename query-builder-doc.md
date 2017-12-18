# Query Builder
- SlackQL has a flexible query builder. However, it enforces strictly about conventions.

### Defining models
- Under a folder named "models" in the project root directory
```python3
  from SlackQL import Model

  class User(Model):
   ...
```

- You can define associations and validations within the model
```pythton3
  from SlackQL import Model

  class User(Model):
    def set_validations(self):
      self.add_validations("name", presence=True)

    def set_associations(self):
      self.has_many("Posts")
      self.has_many("Comments", through="Posts", source="Comments")


### Validations
#### Supported validations:
- presense, uniqueness, inclusion, length, range

### Associations
Note: Conventions come into place the strongest in associations.

#### Rules for defining tables and associations.
There are a few rules in order to make associations in SlackQL works without configurations.
- Table name should be plural, i.e. if you are defining a user table, it should be "users"

Of course, it doesn't always work that way. In those cases where the conventions would create a big hassle, you can specify the primary key and foreign key when you define the association.

When defining your association name:
  - Relationship for has_many should be the pluralized upper CamelCase of the table name
    i.e. for user_groups table - UserGroups
  - Relationship for has_one or belongs_to should be the singularized CamelCase of the table name
    i.e. for user_groups table - UserGroup

Through - the relation that this association will be using
Source - the association name in the class that through leads to
Primary key - default to id ()
Foreign key - default to [singularized table name]_id, i.e. for users table, the foreign key would be user_id

- Has many and has one both have two forms:
```python3
  #has_many<association_name<string>, optional(primary_key=<string>, foreign_key=<string>, foreign_class<string>)>
  #has_many<association_name<string>, through<string>, source<string>>
  self.has_many()
```

### Retrieving multiple rows
- #select<string...>
```python3
  users = User().select('id', 'name')
  >>> SELECT id, name FROM users;
  >>> <class 'Cache'>
  for u in users:
    print(u.name)
```

### To find a single entry
Note: find and find_by triggers queries immediately, therefore, you should chain method prior to calling either methods.
- #find<int> - argument is the id
```python3
  user = User().find(5)
  >>> SELECT * FROM users WHERE id = 5 LIMIT 1;
```

- #find_by<string or kwargs>
```python3
  user = User().find_by(id=5, age=25)
  >>> SELECT * FROM users WHERE id = 5 and age = 25 LIMIT 1;
  >>> <class 'User' {id=5, age=25...}>
  post = Post().where(title="Good Morning").find_by(author="John Doe")
  >>> <class 'Post' {author="John Doe"...}>
```

### Inserting entries
- #insert<kwargs or none> - two ways
1)
```python3
  u = User().insert(name="John Doe", age=25)
  >>> <class 'User' {age=25, name='John Doe'...}>
```
2) ```python3
  u = User()
  u.name = "John Doe"
  u.age = 25
  u.save()
  >>> <class 'User' {age=25, name='John Doe'...}>
```

### Updating entries
- #update
  arguments: none or kwargs of [field]=[value]
1)
```python3
  u = User().find(5)
  >>> <class 'User' {id=5, age=25, name='John Doe'...}>
  u.age = 26
  u.save()
  >>> UPDATE users SET id=5, age=26, name='John Doe' WHERE id = 5;
  >>> <class 'User' {id=5, age=26, name='John Doe'...}>
```
2) ```python3
  u = User().find(5)
  u.update(age=26)
  >>> SELECT * FROM users WHERE id = 5;
  >>> <class 'User' {age=26, name='John Doe'...}>
```

### Clauses

Note: where_not and where(...not=True) are equivalent

- #where and where not
  arguments:
    optional args of strings,
    optional kwargs consists of [field]=[value],
    you can include optional field for "operator" which is defaulted to "=", and "where" also includes optional "is_not" which is not included by default

```python3
  u = User().where(age=25)
  >>> SELECT * FROM users WHERE age = 25;
  u = User().where(age=26, operator="<=", is_not=True)
  >>> SELECT * FROM users WHERE NOT age <= 26;
  u = User().where_not(age=26, operator=">=")
  >>> SELECT * FROM users WHERE NOT age >= 26;
```
Note: between and not_between(...not=True) are equivalent

- #where and where not
  arguments:
    optional args of strings,
    optional kwargs consists of [field]=[value],
    you can include optional field for "operator" which is defaulted to "=", and "where" also includes optional "is_not" which is not included by default

```python3
  u = User().where(age=25)
  >>> SELECT * FROM users WHERE age = 25;
  u = User().where(age=26, operator="<=", is_not=True)
  >>> SELECT * FROM users WHERE NOT age <= 26;
  u = User().where_not(age=26, operator=">=")
  >>> SELECT * FROM users WHERE NOT age >= 26;
```



