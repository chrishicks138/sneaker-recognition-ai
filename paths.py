import os, sys
from config import *
from db import *

class HiddenPrints:

  def __enter__(self):
    self._original_stdout = sys.stdout
    self._original_stderr = sys.stderr
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

  def __exit__(self, exc_type, exc_val, exc_tb):
    sys.stdout.close()
    sys.stderr.close()
    sys.stdout = self._original_stdout
    sys.stderr = self._original_stderr


class ExtractDir:
  def __init__(self, sneaker_brand, sneaker_model):
    self.ipath = os.path.join(IMG_DIR, sneaker_brand, sneaker_model)
    self.tfile = os.path.join(ARC_DIR, sneaker_brand, sneaker_model+ARCHIVE_FORMAT)

  def __rm__(self):
    os.remove(self.tfile)

  def __len__(self):
    return len(os.listdir(self.ipath))

  def __ls__(self):
    return os.listdir(self.ipath)

  def __rmdir__(self):
    for file in os.listdir(self.ipath):
      os.remove(os.path.join(self.ipath, file))
    os.rmdir(self.ipath)

  def archive(self):
    try:
      os.makedirs(self.ipath)
      return self.tfile
    except:
      return self.tfile

  def tpath(self):
    return self.ipath

class ModelDir:
  def __init__(self, sneaker_brand, sneaker_model):
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model

  def __len__(self):
    return len(os.path.join(ORIG_IMG_DIR, self.sneaker_brand, self.sneaker_model))

  def __ls__(self):
    return os.listdir(os.path.join(ORIG_IMG_DIR, self.sneaker_brand, self.sneaker_model))

  def basename(self, f):
    return os.path.basename(f)

  def __rm__(self):
    model_dir = os.path.join(ORIG_IMG_DIR, self.sneaker_brand, self.sneaker_model)
    for file in os.listdir(model_dir):
      os.remove(model_dir+'/'+file)

  def __rmfile__(self, file):
    model_dir = os.path.join(ORIG_IMG_DIR, self.sneaker_brand, self.sneaker_model)
    try:
      os.remove(file)
    except:
      raise

  def __rmdir__(self):
    os.rmdir(os.path.join(ORIG_IMG_DIR, self.sneaker_brand, self.sneaker_model))
  def model_dir(self):
    model_dir = os.path.join(ORIG_IMG_DIR, self.sneaker_brand, self.sneaker_model)
    if not os.path.exists(model_dir):
      os.makedirs(model_dir)
    return model_dir

class ArcDir:
  def __init__(self, sneaker_brand, sneaker_model):
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model
    self.arcdir = ARC_DIR

  def archive_file(self):
    archive = os.path.join(self.arcdir, self.sneaker_model+ARCHIVE_FORMAT)
    return archive

  def __rm__(self):
    archive = os.path.join(self.arcdir, self.sneaker_model+ARCHIVE_FORMAT)
    os.remove(archive)

  def __ls__(self):
    archive_list = os.listdir(self.arcdir)
    return archive_list

  def lsarc(self):
    archive = os.path.join(self.arcdir, self.sneaker_model+ARCHIVE_FORMAT)
    if archive in os.listdir(self.arcdir):
      return True
    else:
      return False
