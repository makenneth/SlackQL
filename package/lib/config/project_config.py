import os, sys, importlib, re, inflection

class Config:
  _loaded = False
  project_path = None

  @classmethod
  def set_project_path(cls, dirname, file):
    file_dir = os.path.dirname(os.path.abspath(file))
    cls.project_path = os.path.join(dirname, file_dir)
    cls.load_files()

  @classmethod
  def load_files(cls):
    if not cls._loaded:
      cls._loaded = True
      name_re = re.compile("^(?!__)(.*).py$")
      model_path = os.path.join(cls.project_path, "models")
      sys.path.append(cls.project_path) # set path to be the main directory for loading modules

      for name in os.listdir(model_path):
        if name_re.match(name):
          model = name[:-3]
          model_class = inflection.camelize(model)
          module = importlib.import_module("models.{}".format(model))

          imported_class = getattr(module, model_class)
          if not imported_class:
            logger.error("Unable to find {} in {}, you may not be able to use associations before to initializing.".format(model_class, model))
          else:
            imported_class()

