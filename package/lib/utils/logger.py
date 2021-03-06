import datetime

class Logger:
  @classmethod
  def current_time(cls):
    return "{0:%H:%M:%S}".format(datetime.datetime.now())

  @classmethod
  def error(cls, error):
    print("\033[1m\033[31m{} - Error: {}\033[0m".format(Logger.current_time(), error))

  @classmethod
  def info(cls, info):
    print("\033[1m\033[32m{} - Info: {}\033[0m".format(Logger.current_time(), info))

  @classmethod
  def warning(cls, warning):
    print("\033[1m\033[33m{} - Warning: {}\033[0m".format(Logger.current_time(), warning))

  @classmethod
  def query(cls, query):
    Logger.info("\033[36m{}".format(query))

  @classmethod
  def complete(cls, start, status):
    Logger.info("Transaction {}: {0:.2f}ms".format(status, (time() - start) * 1000))

  @classmethod
  def time(cls, time):
    Logger.info("\033[0m\033[1m{}".format(time))

  @classmethod
  def representation(cls, string):
    return "\033[1m\033[35m{}\033[0m".format(string)
