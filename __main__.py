import os, sys, argparse
from package.commands import initialize

parser = argparse.ArgumentParser(prog="SlackQL")
parser.add_argument("-m", "--migrate", nargs="*", help="applying migration(s)")
parser.add_argument("-r", "--rollback", nargs="*", help="rollback migration(s)")
# parser.add_argument("-db", "--create", nargs="*", help="create database")
# parser.add_argument("-db", "--reset", nargs="*", help="drop database, create database then apply migrations")
parser.add_argument("-g", "--generate", nargs="*", help="automatically generate file(s). First argument can be 'migration' or 'model'.")
parser.add_argument("-i", "--init", nargs="*", help="create SlackQL related files in your project folder")
parser.add_argument("-d", "--database", type=str, default="psql", choices=["psql", "mysql", "sqlite3"], help="select a db: default to psql")
parser.add_argument("-s", "--spaces", type=int, default=2, help="define the number of spaces when generating files")
args = parser.parse_args()
if args.init:
  # consider moving config to a folder so it can be imported properly
  initialize.initialize_files(args.init, args.database, args.spaces)

elif args.generate:
  if args.generate[0] == "model":
    initialize.create_model(args.generate[1:], args.spaces)
  elif args.generate[0] == "migration":
    initialize.generate_migration(args.generate[1][0], args.spaces)
  else:
    parser.error("Unrecognize generate option {}.".format(args.generate[0]))

# elif args.create:
#   pass
# elif args.reset:
#   pass
elif args.migrate:
  pass

sys.exit(0)
