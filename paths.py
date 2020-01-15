import os
from config import *
import tarfile

class Path:

  def __init__(self):
    super().__init__()

  def ipath(self, tfile):
    amodel = tfile.split('/')[4]
    model = amodel.split('.')[0]
    brand = tfile.split('/')[3]
    ipath = os.path.join(IMG_DIR, brand, model)
    if not os.path.exists(ipath):
      os.makedirs(ipath)
    try:
      with tarfile.open(tfile) as tar:
        tar.extractall(ipath)
    except:
      raise

  def model_dir(self, sneaker_brand, sneaker_model):
    model_dir = os.path.join(ORIG_IMG_DIR, sneaker_brand, sneaker_model)
    if not os.path.exists(model_dir):
      os.makedirs(model_dir)
    return os.path.join(ORIG_IMG_DIR, sneaker_brand, sneaker_model)


  def arc_dir(self, sneaker_brand, sneaker_model):
    arcdir = os.path.join(ARC_DIR, sneaker_brand)
    if not os.path.exists(arcdir):
      os.makedirs(arcdir)

  def lsarc(self, sneaker_model, sneaker_brand):
    if sneaker_model+'.tar.bz2' in os.listdir(os.path.join(ARC_DIR, sneaker_brand)):
      return True
    else:
      return False
