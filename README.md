# SlackQL
ActiveRecord in Python.

## Todo
- [ ] support for psql
- [ ] tests

- Find
```python
>>> p = Post.find(5)
>>> print p
<class 'Post' {id=5, title="Hello world" ...}>
```

- Find_by
```python
>>> p = Post.find_by(title="Hello world")
<class 'Post' {id=3, title="Hello world" ...}>
```

## Lazy Evaluation
```python
>>> Post.select("title", "body").order(DESC="id").limit(1)
[<class 'Post' {id=5, title="Hello world" ...}>]
```

- Select
```python
>>> Post.select("title", "body")
"SELECT title, body FROM post"
[<class 'POST' {title="xxxx", body="xxxx"}..]
```

- Where 
```python
>>> Post.where(title="Hello world") 
>>> Post.where("title = Hello world")
"SELECT * FROM post where title = 'Hello World'"
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


## Validations
- Uniqueness - Argument: True or False
```python
  add_validations("color", unique=True)
```

- Presence - Argument: True or False
```python
  add_validations("color", presence=True)
```

- Inclusion - Argument: list of choices
```python
  add_validations("color", inclusion=["brown", "white", "blue"])
```

- Length
```python
  add_validations("password", length={"min": 5, "max": 10})
```

- Allow None
