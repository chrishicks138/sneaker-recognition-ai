import os, sys
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
  def __init__(self):
    super().__init__()

  def download(self, sneaker_brand, sneaker_model):
    self.prestatus = 'Downloading'
    search = sneaker_brand+' '+sneaker_model
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model
    s = search.replace(' ','/')
    print('\n'+search)
    model_dir = os.path.join(ORIG_IMG_DIR, s)
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

    Convert().convert(model_dir, sneaker_brand, sneaker_model)

  def download_images(self, sneakers):
    shoes = []
    print('\n')
    self.prestatus = 'Searching'
    self.m = 0
    antiTraversal = ['../', 'cat ../', 'cat ', ]
    path = DATA_DIR+'/shoes.txt'
    for shoe in sneakers:
      for traversal in antiTraversal:
        if traversal not in shoe:
          shoes.append(shoe)
    for shoe in shoes:
      self.bt = len(shoes)
      sneaker_model_names = shoe.split('_')
      sneaker_brand = sneaker_model_names[0];
      sneaker_model = sneaker_model_names[1];
      sneaker_model = sneaker_model.replace('\n','')
      model_dir = os.path.join(ORIG_IMG_DIR, sneaker_brand, sneaker_model);
      self.m = 1+self.m
      self.status = str(self.m)+'/'+str(self.bt)
      self.log_batch_index = self.m
      self.log_batch_size = self.bt
      Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
      if not os.path.exists(model_dir):
        os.makedirs(model_dir);
      arcdir = os.path.join(ARC_DIR, sneaker_brand)
      if not os.path.exists(arcdir):
        os.makedirs(arcdir)
        if (sneaker_model+'.tar.bz2') in os.listdir(arcdir):
          print('Archive found! Skipping...')
          continue
        else:
          samples.download(sneaker_brand, sneaker_model)
      continue

samples = Samples()
