import os, sys, inflection

def create_models(models, spaces):
  if not os.path.exists("models2"):
    print("Creating models directory...")
    os.mkdir("models2")

  with open("./models2/__init__.py", "w+") as f:
    pass

  for model in models:
    with open("./models2/{}.py".format(inflection.singularize(model)), "w+") as f:
      f.writelines([
        "from SlackQL import Model\n\n",
        "class {}(Model):\n".format(inflection.camelize(inflection.singularize(model))),
        "{}def set_associations(self):\n".format(" " * spaces * 1),
        "{}pass\n".format(" " * spaces * 2),
        "\n",
        "{}def set_validations(self):\n".format(" " * spaces * 1),
        "{}pass\n".format(" " * spaces * 2),
        "\n",
      ])
    print("Done.")

def initialize_files(models, db, spaces):
  current_path = os.getcwd()
  sys.path.append(current_path)
  print("Creating files...")
  create_models(models, spaces)

  if not os.path.exists("migration"):
    print("Creating migration directory...")
    os.mkdir("migration")

  with open("./slackql_init.py", "w+") as f:
    db_config = None
    if db == "psql":
      db_config = "database_engine=\"psql\", port=\"5432\", localhost=\"localhost\", username=\"\", password=\"\""
    elif db == "mysql":
      db_config = "database_engine=\"psql\", port=\"3306\", localhost=\"localhost\", username=\"\", password=\"\""
    else:
      db_config = "db_name"

    f.writelines([
      "import SlackQL\n",
      "SlackQL.set_project_path(\".\", __file__)\n",
      "SlackQL.configure({})\n".format(db_config),
      "\n"
    ])

  print("Done.")
  print("Please change the database settings in slackql_init.py before running migrations.")
