# SlackQL
[![Build Status](https://travis-ci.org/makenneth/SlackQL.svg?branch=master)](https://travis-ci.org/makenneth/SlackQL)[![Coverage Status](https://coveralls.io/repos/github/makenneth/SlackQL/badge.svg)](https://coveralls.io/github/makenneth/SlackQL)

Python ORM (ActiveRecord) - largely inspired by ActiveRecord in Ruby on Rails. Just like in Ruby on Rails, this ActiveRecord utilizes lazy evaluations, which allows method to be chainable.

## Basic Usage
### Configuration
Before running any queries, you have to:
1) set the base project path
2) configure the connection with the database of choice.

```python
# bin/setup.py
import SlackQL
#set_project_path(rel path, __file__)
SlackQL.set_project_path("..", __file__)
SlackQL.configure(database_engine="psql", db_name="twitter")
```
Note: The config file can be named anything and located anywhere, as long as it is called when your server starts.

sqlite3 database will be created at the base path with a name defaulted to name of the project folder.
parameters:
  - database_engine (currently support: psql,mysql,sqlite3)
  - db_name
  - username (default to "")
  - password (default to "")
  - connection_timeout
  - host (default to localhost)
  - port (default to database default port)

### Defining a Model
model has to be placed in a folder named "models" with __init__ and be placed in the project root directory

```python
# models/user.py
from SlackQL import Model
class User(Model):
  def set_validations(self):
    self.add_validations("name", presence=True)

  def set_associations(self):
    self.has_many("Posts")
    self.belongs_to("Group")
```

### Basic Lookup
- Find
```python
>>> p = Post.find(5)
<class 'Post' {id=5, title="Hello world" ...}>
```

- Find_by
```python
>>> p = Post.find_by(title="Hello world")
<class 'Post' {id=3, title="Hello world" ...}>
```

## Appending and Editing
- Create New
```python
from models import Post
>>> p = Post(title="Bye World")
>>> p.body = "test body"
>>> p.save()
<class 'Post' {id=4, title="Bye World" ...}>
```

- Edit
```python
from models import Post
>>> p = Post.find(4)
<class 'Post' {id=4, title="Bye World" ...}>
>>> p.title = "Hi World"
>>> p.save()
<class 'Post' {id=4, title="Hi World" ...}>
```

### Lazy Evaluation
```python
>>> Post.select("title", "body").order(DESC="id").limit(1)
[<class 'Post' {id=5, title="Hello world" ...}>]
```

- Select
```python
>>> Post.select("title", "body")
"SELECT title, body FROM posts"
[<class 'POST' {title="xxxx", body="xxxx"}..]
```

- Where
```python
>>> Post.where(title="Hello world")
>>> Post.where("title = Hello world")
"SELECT * FROM posts where title = 'Hello World'"
[<class 'Post' {id=5, title="Hello world" ...}>...]
```

- Order
```python
>>> Post.order("ASC=title").order(DESC="body")
>>> Post.order("ASC=title").order(ASC="body")
```
- Limit
```python
Posts.limit(5)
```

### Validations
```python
  # Uniqueness - Argument: True or False
  add_validations("color", uniqueness=True)

  # Presence - Argument: True or False
  add_validations("color", presence=True)

  # Inclusion - Argument: list of choices
  add_validations("color", inclusion=["brown", "white", "blue"])

  # Length - Can only be applied on strings/arrays - Argument: dict with max and mean
  add_validations("password", length={"min": 5, "max": 10})

  # Range - Can only be applied on numbers - Argument: dict with max and mean
  add_validations("age", length={"min": 18, "max": 66})
```

#### Todo
- [ ] aggregates
- [ ] more options: "LIKE"
- [ ] migrations
- [ ] check support for psql, mysql, sqlite3...
- [ ] more tests
