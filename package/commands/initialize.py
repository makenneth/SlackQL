import os, sys, inflection
import re
from datetime import datetime
def create_model(models, spaces):
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

  if not os.path.exists("migrations"):
    print("Creating migration directory...")
    os.mkdir("migrations")

  if not os.path.exists("config"):
    print("Creating config directory...")
    os.mkdir("config")

  with open("./config/slackql.yml", "w+") as f:
    lines = []
    if db == "psql":
      lines = [
        "database_engine: \"psql\"\n",
        "port: 5432\n",
        "localhost: \"localhost\"\n",
        "username: \"\"\n",
        "password: \"\"\n",
      ]
    elif db == "mysql":
      lines = [
        "database_engine: \"mysql\"\n",
        "port: 3306\n",
        "localhost: \"localhost\"\n",
        "username: \"\"\n",
        "password: \"\"\n",
      ]
    else:
      lines = ["db_name"]
    f.writelines(lines)

  with open("./slackql_init.py", "w+") as f:
    f.writelines([
      "import yaml\n",
      "import SlackQL\n",
      "SlackQL.set_project_path(\".\", __file__)\n",
      "with open(\"./config/slackql.yml\", \"r\") as stream:\n",
      "{}SlackQL.configure(yaml.load(stream))\n".format(" " * spaces * 1)
    ])

  print("Files generated :).")
  print("Please change the database settings in config/slackql.py before running migrations.")

def generate_migration(name, spaces):
  current_path = os.getcwd()
  sys.path.append(current_path)
  date = re.sub(r"[-:.\s]", "", str(datetime.now())[0:-4])
  file_name = "{}_migration".format(date)
  with open("./migrations/{}.py".format(file_name), "w+") as f:
    f.writelines([
      "from SlackQL import Migration, Column\n\n",
      "class {}{}(Migration):\n".format(name, date),
      "{}def change(self):\n".format(" " * spaces * 1),
      "{}pass".format(" " * spaces * 2)
    ])
    print("created migration file")
