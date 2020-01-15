import sys
from data_transform import *;
from config import *;
from google_images_download import google_images_download as gid
from trainer import *
from progress import *
from tempfile import mkstemp
from archive import *
from convert import *

class HiddenPrints:
  def __init__(self):
    self.data = []

  def write(self, s):
    self.data.append(s)

  def __enter__(self):
    sys.stdout = self
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    sys.stdout = sys.__stdout__

class Samples:
  def __init__(self, sneaker_brand, sneaker_model):
    super().__init__()
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model
    self.mdir = ModelDir(sneaker_brand, sneaker_model)
    try:
      ArcDir().arc_dir(self.sneaker_brand, self.sneaker_model)
      if ArcDir().lsarc(self.sneaker_model, self.sneaker_brand) is False:
        self.download()
      else:
        return
    except:
      raise


  def download(self):
    self.prestatus = 'Downloading'
    search = self.sneaker_brand+' '+self.sneaker_model
    s = search.replace(' ','/')
    print('\n'+search)
    model_dir = self.mdir.model_dir()
    resp = gid.googleimagesdownload()
    with HiddenPrints() as x:
      aip, data = resp.download({"keywords":search,"format":"jpg","limit":LIMIT,"aspect_ratio":"square","output_directory":model_dir,"no_directory":"1"})
    for data in aip:
      self.bt = len(aip[data])
      self.m = 0
      self.log_batch_index = self.m
      self.log_batch_size = self.bt
      for i in aip[data]:
        self.m = self.m+1
        self.status = str(self.m)
        Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
    Convert(self.sneaker_brand, self.sneaker_model).convert()

