import os, sys, argparse
from package.commands import initialize

parser = argparse.ArgumentParser(prog="SlackQL")
parser.add_argument("-m", "--migrate", type=str, help="applying migration(s)")
parser.add_argument("-g", "--generate", nargs="*", help="automatically generate file(s). First argument can be 'migration' or 'model'.")
parser.add_argument("-i", "--init", nargs="*", help="create SlackQL related files in your project folder")

parser.add_argument("-d", "--database", type=str, default="psql", choices=["psql", "mysql", "sqlite3"], help="select a db: default to psql")
parser.add_argument("-s", "--spaces", type=int, default=2, help="define the number of spaces when generating files")
args = parser.parse_args()

if args.init:
  initialize.initialize_files(args.init, args.database, args.spaces)

if args.generate:
  if args.generate[0] == "model":
    initialize.create_models(args.generate[1:], args.spaces)
  elif args.generate[0] == "migration":
    pass
  else:
    parser.error("Unrecognize generate option {}.".format(args.generate[0]))
sys.exit(0)
