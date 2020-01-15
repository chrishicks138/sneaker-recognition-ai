import tarfile
import os, sys
from data_transform import *;
from config import *;
from trainer import *
from progress import *
from tempfile import mkstemp
from progress import *

class Archive:
  def __init__(self):
    super().__init__()

  def archive_prep(self, sneaker_brand, sneaker_model, model_dir):
    files = []
    self.files = files
    self.model_dir = model_dir
    for d in os.listdir(self.model_dir):
      if 'tar.bz2' not in d:
        if '.jpg' in d:
          files.append(os.path.join(self.model_dir, d))
    Archive().archive(sneaker_brand, sneaker_model, model_dir, files)

  def archive(self, sneaker_brand, sneaker_model, model_dir, files):
    arcdir = os.path.join(ARC_DIR, sneaker_brand)
    if not os.path.exists(arcdir):
      os.makedirs(arcdir)
    tfile = arcdir+'/'+sneaker_model+'.tar.bz2'
#    tfd, tfile = mkstemp()
    with tarfile.open(tfile, "w:bz2") as tar:
      c = 0
      for f in files:
        c = 1+c
        self.bt = len(files)
        self.m = c
        self.prestatus = 'Archiving'
        self.status = str(c)
        self.log_batch_index = c
        self.log_batch_size = len(files)
        Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
        image = os.path.basename(f)
        tar.add(f, arcname=image)
        os.remove(f)
      tar.close()
#    print(str(c)+' FILES ARCHIVED\n')
    Trainer().run(tfile, sneaker_brand, sneaker_model)
    try:
      for f in os.listdir(model_dir):
        os.remove(model_dir+'/'+f)
      os.rmdir(model_dir)
    except:
      print('\r'+model_dir+' NOT FOUND!')
      return

