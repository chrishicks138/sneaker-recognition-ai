
import tarfile
import sys
from data_transform import *;
from config import *;
from trainer import *
from progress import *
from tempfile import mkstemp
from progress import *

class Archive:
  def __init__(self, sneaker_brand, sneaker_model):
    super().__init__()
    self.ArcDir = ArcDir(sneaker_brand, sneaker_model)
    self.extract = ExtractDir(sneaker_brand, sneaker_model)
    self.mdir = ModelDir(sneaker_brand, sneaker_model)
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model

  def archive_prep(self):
    files = []
    for d in self.mdir.__ls__():
      if ARCHIVE_FORMAT not in d:
        if IMAGE_FORMAT in d:
          files.append(self.mdir.model_dir()+'/'+d)
    Archive(self.sneaker_brand, self.sneaker_model).archive(files)

  def archive(self, files):
    self.ArcDir.arc_dir()
#    tfd, tfile = mkstemp()
    archive_file = self.ArcDir.archive_file()
    self.bt = len(files)
    c = 0
    with tarfile.open(archive_file, "w|gz") as tar:
      for f in files:
        c = c+1
        image = self.mdir.basename(f)
        tar.add(f, arcname=image)
        self.m = c
        self.prestatus = 'Archiving'
        self.status = str(c)
        self.log_batch_index = c
        self.log_batch_size = len(files)
        Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
        self.mdir.__rmfile__(f)
#    print(str(c)+' FILES ARCHIVED\n')
    try:
      for f in self.mdir.model_dir():
        self.mdir.__rmfile__(f)
      self.mdir.__rmfile__(f)
    except:
      print('\r'+self.mdir.model_dir()+' NOT FOUND!')
      return

