# SlackQL
Python ORM (ActiveRecord) - largely inspired by ActiveRecord in Ruby on Rails. Just like Ruby on Rails, this ActiveRecord utilizes lazy evaluations, which allows method to be chainable.

## Basic Usage
### Configuration
Before running any queries, simply call SlackQL.configure once to configure the connection.
```python
import SlackQL
SlackQL.configure(database_engine="psql", db_name="twitter")
```

parameters:
  - database_engine (currently support: psql,mysql,sqlite3)
  - db_name
  - username (default to "")
  - password (default to "")
  - connection_timeout
  - host (default to localhost)
  - port (default to database default port)


### Defining a Model
```python
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
- [ ] associations
- [ ] migrations
- [ ] check support for psql, mysql, sqlite3...
- [ ] more tests
