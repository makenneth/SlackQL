import os, sys, inflection

def prepare_db():
  pass
  # get db config -> should switch to .yaml

def generate_migration():
  current_path = os.getcwd()
  sys.path.append(current_path)
  prepare_db()
