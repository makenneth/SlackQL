import os, sys, inflection
from datetime import datetime

def prepare_db(create_db):
  pass
  # get db config -> should switch to .yaml

def generate_migration(spaces):
  current_path = os.getcwd()
  sys.path.append(current_path)
  date = re.sub(r"[-:.\s]", "", str(datetime.now())[0:-4])
  file_name = "{}_migration".format(date)
  with open("./migration/{}.py".format(file_name), "w+") as f:
    f.writelines([
      "from SlackQL import Migration, Column\n\n",
      "class Migration{}(Migration):\n".format(file_name),
      "{}def change(self):\n".format(" " * spaces * 1),
      "{}pass".format(" " * spaces * 2)
    ])
    print("created migration file")
